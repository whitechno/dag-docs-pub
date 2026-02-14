---
prev-chapter: "Key Related Works"
prev-url: "02-related-works"
page-title: Training Overview
next-chapter: "Instruction Tuning"
next-url: "04-instruction-tuning"
---

# Training Overview

In this chapter we provide a cursory overview of RLHF training, before getting
into the specifics later in the book. RLHF, while optimizing a simple loss
function, involves training multiple, different AI models in sequence and then
linking them together in a complex, online optimization.

Here, we introduce the core objective of RLHF, which is optimizing a proxy
reward for human preferences with a distance-based regularizer (along with
showing how it relates to classical RL problems). Then we showcase canonical
recipes which use RLHF to create leading models to show how RLHF fits in with
the rest of post-training methods. These example recipes will serve as
references for later in the book, where we describe different optimization
choices you have when doing RLHF, and we will point back to how different key
models used different steps in training.

## Problem Formulation

The optimization of reinforcement learning from human feedback (RLHF) builds on
top of the standard RL setup. In RL, an agent takes actions $a_t$ sampled from a
policy $\pi(a_t\mid s_t)$ given the state of the environment $s_t$ to maximize
reward $r(s_t,a_t)$ [@sutton2018reinforcement]. Traditionally, the environment
evolves according to transition (dynamics) $p(s_{t+1}\mid s_t, a_t)$ with an
initial state distribution $\rho_0(s_0)$. Together, the policy and dynamics
induce a trajectory distribution:

$$p_{\pi}(\tau)=\rho_0(s_0)\prod_{t=0}^{T-1}\pi(a_t\mid s_t)\,p(s_{t+1}\mid s_t,a_t).$$
{#eq:rl_dynam}

Across a finite episode with horizon $T$, the goal of an RL agent is to solve
the following optimization:

$$J(\pi) = \mathbb{E}_{\tau \sim p_{\pi}} \left[ \sum_{t=0}^{T-1} \gamma^t r(s_t, a_t) \right],$$
{#eq:rl_opt}

For continuing tasks, one often takes $T\to\infty$ and relies on
discounting ($\gamma<1$) to keep the objective well-defined.
$\gamma$ is a discount factor from 0 to 1 that balances the desirability of
near-term versus future rewards. Multiple methods for optimizing this expression
are discussed in Chapter 6.

![Standard RL loop](../images/rl.png){#fig:rl width=320px .center}

A standard illustration of the RL loop is shown in @fig:rl (compare this to the
RLHF loop in @fig:rlhf).

### A Simple Example: The Thermostat {#example-rl-thermostat}

To build a basic intuition for what RL does, consider a thermostat trying to
keep a room at a target temperature of 70$^\circ$F. In RL, the agent starts with
no knowledge of the task and must discover a good policy through trial and
error. The thermostat example has the following components
(see @fig:thermostat-equation for how each maps to the trajectory distribution
in @eq:rl_dynam):

- **State ($s_t$)**: the current room temperature, e.g. 65$^\circ$F.
- **Action ($a_t$)**: turn the heater on or off.
- **Reward ($r$)**: +1 when the temperature is within 2$^\circ$ of the target, 0
  otherwise.
- **Policy ($\pi$)**: the rule that decides whether to turn the heater on or off
  given the current temperature. An example policy, which may not be optimal
  depending on the exact transition dynamics of the environment:

$$\pi(a_t = \text{on} \mid s_t) = \begin{cases} 1 & \text{if } s_t < 70^{\circ}\text{F} \\ 0 & \text{otherwise} \end{cases}$$
{#eq:thermostat_policy}

- **Transition**: the room warms when the heater is on and cools when it is
  off -- this is the environment dynamics that the agent cannot control
  directly.

![Each term in the trajectory distribution (@eq:rl_dynam) mapped to the thermostat RL example.](
../images/thermostat_equation.png){#fig:thermostat-equation .center}

Initially, the thermostat's policy is essentially random -- it flips the heater
on and off with no regard for the current temperature, and the room swings
wildly. Over many episodes of trial and error, the agent discovers that turning
the heater on when the room is cold and off when it is warm leads to more
reward, and gradually converges on a sensible policy. This is the core RL loop:
observe a state, choose an action, receive a reward, and update the policy to
get more reward over time.

### Example RL Task: CartPole

For a richer example with continuous dynamics, consider the classic *CartPole*
(inverted pendulum) control task, which appears in many RL textbooks, courses,
and even research papers. Where the thermostat had a single state variable and a
binary action, CartPole involves four continuous state variables and
physics-based transitions -- making it a standard benchmark for RL algorithms.

![CartPole environment showing state variables ($x$, $\dot{x}$, $\theta$, $\dot{\theta}$) and actions ($\pm F$).](
../images/cartpole.png){#fig:cartpole width=400px .center}

- **State ($s_t$)**: the cart position/velocity and pole angle/angular velocity,

  $$s_t = (x_t,\,\dot{x}_t,\,\theta_t,\,\dot{\theta}_t).$$ {#eq:cartpole_state}

- **Action ($a_t$)**: apply a left/right horizontal force to the cart,
  e.g. $a_t \in \{-F, +F\}$.

- **Reward ($r$)**: a simple reward is $r_t = 1$ each step the pole remains
  balanced and the cart stays on the track (e.g. $|x_t| \le 2.4$
  and $|\theta_t| \le 12^\circ$), and the episode terminates when either bound
  is violated.

- **Dynamics / transition ($p(s_{t+1}\mid s_t,a_t)$)**: in many environments the
  dynamics are deterministic (so $p$ is a point mass) and can be written
  as $s_{t+1} = f(s_t,a_t)$ via Euler integration with step size $\Delta t$. A
  standard simplified CartPole update uses constants cart mass $m_c$, pole
  mass $m_p$, pole half-length $l$, and gravity $g$:

  $$\text{temp} = \frac{a_t + m_p l\,\dot{\theta}_t^2\sin\theta_t}{m_c + m_p}$$
  {#eq:cartpole_temp}

  $$\ddot{\theta}_t = \frac{g\sin\theta_t - \cos\theta_t\,\text{temp}}{l\left(\tfrac{4}{3} - \frac{m_p\cos^2\theta_t}{m_c + m_p}\right)}$$
  {#eq:cartpole_angular_accel}

  $$\ddot{x}_t = \text{temp} - \frac{m_p l\,\ddot{\theta}_t\cos\theta_t}{m_c + m_p}$$
  {#eq:cartpole_linear_accel}

  $$x_{t+1}=x_t+\Delta t\,\dot{x}_t,\quad \dot{x}_{t+1}=\dot{x}_t+\Delta t\,\ddot{x}_t,$$
  {#eq:cartpole_pos_update}
  $$\theta_{t+1}=\theta_t+\Delta t\,\dot{\theta}_t,\quad \dot{\theta}_{t+1}=\dot{\theta}_t+\Delta t\,\ddot{\theta}_t.$$
  {#eq:cartpole_angle_update}

This is a concrete instance of the general setup above: the policy
chooses $a_t$, the transition function advances the state, and the reward is
accumulated over the episode.

### Manipulating the Standard RL Setup

The RL formulation for RLHF is seen as a less open-ended problem, where a few
key pieces of RL are set to specific definitions in order to accommodate
language models. There are multiple core changes from the standard RL setup to
that of RLHF:
Table @tbl:rl-vs-rlhf summarizes these differences between standard RL and the
RLHF setup used for language models.

1. **Switching from a reward function to a reward model.** In RLHF, a learned
   model of human preferences, $r_\theta(s_t, a_t)$ (or any other classification
   model) is used instead of an environmental reward function. This gives the
   designer a substantial increase in the flexibility of the approach and
   control over the final results, but at the cost of implementation complexity.
   In standard RL, the reward is seen as a static piece of the environment that
   cannot be changed or manipulated by the person designing the learning agent.
2. **No state transitions exist.** In RLHF, the initial states for the domain
   are prompts sampled from a training dataset and the "action" is the
   completion to said prompt. During standard practices, this action does not
   impact the next state and is only scored by the reward model.
3. **Response level rewards.** Often referred to as a bandit problem, RLHF
   attribution of reward is done for an entire sequence of actions, composed of
   multiple generated tokens, rather than in a fine-grained manner.

::: {.table-wrap}

| Aspect             | Standard RL                              | RLHF (language models)                                                                           |
|--------------------|------------------------------------------|--------------------------------------------------------------------------------------------------|
| Reward signal      | Environment reward function $r(s_t,a_t)$ | Learned reward / preference model $r_\theta(x,y)$ (prompt $x$, completion $y$)                   |
| State transition   | Yes: dynamics $p(s_{t+1}\mid s_t,a_t)$   | Typically no: prompts $x$ sampled from a dataset; the completion does not define the next prompt |
| Action             | Single environment action $a_t$          | A completion $y$ (a sequence of tokens) sampled from $\pi_\theta(\cdot\mid x)$                   |
| Reward granularity | Often per-step / fine-grained            | Usually response-level (bandit-style) over the full completion                                   |
| Horizon            | Multi-step episode ($T>1$)               | Often single-step ($T=1$), though multi-turn can be modeled as longer-horizon                    |

Table: Key differences between standard RL and RLHF for language models.  
{#tbl:rl-vs-rlhf}
:::

Given the single-turn nature of the problem, the optimization can be re-written
without the time horizon and discount factor (and with an explicit reward
model):
$$J(\pi) = \mathbb{E}_{\tau \sim \pi} \left[r_\theta(s_t, a_t) \right].$$
{#eq:rl_opt_int}

In many ways, the result is that while RLHF is heavily inspired by RL optimizers
and problem formulations, the actual implementation is very distinct from
traditional RL.

![Standard RLHF loop](../images/rlhf.png){#fig:rlhf width=320px .center}

