# Crowd Evacuation Conflicts Simulation Based Cellular Automaton Integrating Game Theory

- Junxiao Xue
- Haozhe Yang
- Mingchuang Zhang
- Zekun Wang
- Lei Shi

## ABSTRACT

Developing and rehearsing crowd evacuation plans in crowd gathering situations can improve evacuation efficiency and reduce safety accidents. However, pedestrians can create resource conflicts with other pedestrians competing for evacuation routes during crowd evacuation. Inspired by cellular automata and game theory, this paper proposes a crowd evacuation model that integrates cellular automata and game theory to solve the conflicts among pedestrians in the evacuation process. In the model construction, we construct a basic crowd evacuation model using a cellular automaton, formulate a game rule for pedestrians’ conflict according to the prisoner’s dilemma, and integrate the pedestrians’ update strategy into the cellular automaton. The model’s validity is verified in the experiments by comparing the update and non-update strategies, and the crowd evacuation is visualized and simulated by constructing a stadium scenario. The experimental results show that the crowd evacuation model incorporating the pedestrian conflict game rules is more realistic and will improve the crowd evacuation efficiency if the pedestrians adopt the cooperative strategy

## CCS CONCEPTS

- Computing methodologies → Modeling and simulation

## KEYWORDS

Game Theory, Cellular Automata, Emergency Evacuation, Swarm Simulation

## 1 INTRODUCTION

Nowadays, the rapid development of urbanization leads to frequent crowd-gathering activities. With the high density of people in significant public places and the complex structure of crowds, the absence of a reasonable and efficient crowd evacuation plan will result in serious safety accidents such as stampedes when an emergency occurs. In the typical evacuation process, conflicts will inevitably occur when two or more pedestrians choose the same place at the exact moment. Crowd conflicts frequently occur during evacuations between pedestrians, especially at high-density exit bottlenecks. These conflicts significantly impact evacuation times, exit throughput, and the design and optimization of the building’s internal structure [Xie et al. 2021]. For example, on September 24, 2015, at least 1399 people were killed and more than 2000 injured in the Mecca Minar area of Saudi Arabia due to a stampede that occurred when some pilgrims did not act as required. Therefore, finding an appropriate method to understand the evolution of evacuation conflicts is essential to develop and rehearsing a reasonable and efficient crowd evacuation plan.

There are already many researchers who have conducted studies on crowd evacuation. Wagneretal [WagnerandAgrawal2014] proposed a prototype agent-based crowd evacuation simulation system for concert venues to model crowd evacuation under fire disasters. Liu et al. [Liu et al. 2018] proposed a crowd evacuation simulation method based on navigation knowledge and a two-level control mechanism to decompose the large-scale evacuation problem into sub-problems and effectively improve evacuation efficiency. Yao et al. [Yao et al. 2019] proposed a data-driven crowd evacuation framework based on reinforcement learning for simulating actual crowd evacuation behavior in dynamic environments, improving crowd evacuation’s visual realism and path computation efficiency. Han and Liu [HanandLiu2017] introduced an information transfer mechanism into the social force model to simulate crowd behavior. Dang et al. [Dang et al. 2021] proposed a virtual reality large-scale crowd evacuation chain navigation grid based on beta cellular automata to improve crowd evacuation efficiency.

In previous studies of crowd evacuation, scholars have viewed crowd as identical individuals, ignoring the differences among individuals. However, people with different attributes adopt different strategies when faced with conflict. Generally, when conflict occurs, pedestrians adopt two strategies: cooperative strategy, in which pedestrians comply with the order, and competitive strategy, in which pedestrians do not comply with the evacuation order. This paper considers the different behavioral manifestations of pedestrians adopting competitive and cooperative strategies when conflicts occur in a realistic evacuation process. We combine a cellular automata model with game theory to solve the conflict problem in the evacuation process. The main contributions of this paper are as follows.

- We propose cellular automata crowd evacuation model in cooperating game theory.
- We introduce penalty factors and inertia indices in the model to develop pedestrian location conflict rules to solve the conflict problem arising from crowd evacuation.
- By conducting a crowd evacuation simulation in a stadium scenario, we propose a solution to improve the efficiency of crowd evacuation: pedestrians should adopt a cooperative strategy.

The remaining parts of the paper are as follows: Section 2 introduces the related work of the paper. Section 3 describes the model’s construction method and derivation process in detail. The experimental part and the conclusion are presented in Sections 4 and 5, respectively.

## 2 RELATED WORKS

### 2.1 Pedestrian Behavior Characteristics

The diversity of pedestrian attributes directly affects the diversity of evacuation behavior. Therefore, these factors need to be considered in the model in the actual simulation. Therefore, it is necessary to study the behavior characteristics of pedestrians and the factors that affect pedestrian behavior. After an emergency occurs, pedestrians will show a variety of complex psychological reactions, and these complex psychological reactions will have a significant impact on the evacuation results [Al-Gadhi 1996; Gupta and Pundir 2015; Xue et al. 2019, 2021]. The typical psychology in the evacuation mainly includes the following:

1. Herd mentality [Spence 2011]: Especially when pedestrians feel unfamiliar with the surrounding environment, they will evacuate with the people around them. In psychology, this phenomenon is also called the herd effect. During the evacuation, this mentality often manifests as following the route of most pedestrians. However, this blind obedience often causes congestion at the exit.

2. Panic psychology [Aguirre 2005]: When an emergency occurs without warning, the evacuees will panic because they are unprepared, which is caused by people’s lack of knowledge and experience of safe evacuation and unfamiliarity with the environment. This psychological mechanism will reduce the decision-making ability of pedestrians to evacuate and promote the phenomenon of congestion and congestion.

3. Impulsive psychology [Frijda 2010]: When the density of pedestrians is high and the space is narrow, it is easy to cause congestion, and pedestrians will unconsciously and eagerly leave the crowd. The greater the congestion, the higher the chance of casualties.

4. Sympathy and helping psychology [Tugarinov et al. 2020]: Social psychology studies have found that in many evacuation scenarios, some people will help the weak around them, such as the elderly and children, and not everyone is selfish.

### 2.2 Evacuation Pedestrian Decision Behavior

When emergencies occur, pedestrians will subjectively estimate the degree of danger and the surrounding environment and make corresponding decisions. When emergencies occur, pedestrians’ cognitions come from past experiences and the information they can receive at that time, leading to differences in the judgment and decision-making of different personnel on the information. Pedestrians’ decision-making in the evacuation process will be affected by many factors, and the influence of various factors on evacuation is nonlinear, so the behavioural decision-making of pedestrians is complex [Heliovaara et al. 2012; Li et al. 2017b,a].

In modelling pedestrian choice behaviour, commonly used methods include random utility theory and multiple logarithmic models. Song et al. [Wei-Guo et al. 2006] improved the static field value calculation method in the field model based on cellular automata and studied the indoor multi-exit evacuation problem with obstacles. Liu et al. [Liu et al. 2011] introduced the exit spare capacity, discussed the attractiveness of the spare capacity to pedestrians, and applied the extended cellular automata model to study the typical behavior characteristics of crowd evacuation. Xu and Huang [Xu and Huang 2012] studied the pedestrian exit selection behavior in multi-exit rooms and introduced a directional view field into the model. Yue et al. [Yue et al. 2011] proposed a pedestrian dynamic parameter simulation model, and studied the evacuation characteristics of pedestrian flow under the conditions of the unbalanced initial position of pedestrians and affected pedestrian sight lines.

### 2.3 Pedestrian Evacuation Based on Game Theory

For the study of pedestrian decision-making behavior, the method of game theory is often used. Game theory is that players choose their acceptable strategies in an equal game, and use the opponent’s strategy to change their confrontation strategies accordingly, to achieve the goal of the greatest possibility of winning. In terms of conflict games, Zhengetal.[Zhengetal.2019] established an escape game model combining cellular automata and game theory to study the effect of pedestrian herding and rationality on cooperative evolution and evacuation mechanism during evacuation. Shi et al. [Shi et al. 2017] combined the lattice gas model to introduce the indirect cost-benefit ratio into the snowdrift model to simulate the fear index of pedestrians, and to introduce the possibility of changing the current strategy to simulate the strategy choice of pedestrians. Schantz et al. [von Schantz and Ehtamo 2019] proposed a calculation based on cellular automata combined with spatial games to resolve conflict situations between panicked people, in addition, to adding topological structure and behavioral features, and adding different movement speeds and memory features to evacuees.

## 3 METHODOLOGY

The cellular automata model is a commonly used model for studying evacuation dynamics. In this paper, a two-dimensional square grid is used to describe the room, each grid size is 0.4 ∗ 0.4 m2, and the grid can only be occupied by one pedestrian, or by the space boundary, or it can be empty.

The motion of pedestrian $i$ is determined by the static field value $SF(i)$, which is measured by the inverse of the distance from grid i to the exit $e_k$, where $(x_{ek}, y_{ek})$, is the exit The coordinates of $(x_i,y_i)$ are the coordinates of pedestrian i. The calculation formula of static field value is shown in formula (1):

$$
SF_{(i)} = \frac{1}{\sqrt{(x_{ek} - x_i)^2 + (y_{ek} - y_i)^2}}
$$

At each time step, there may be a certain number of empty grids near pedestrians. Therefore, the probability of pedestrian I moving to grid j (near it) is calculated according to the following formula (2).

$$
P_{(i \to j)} = \frac{\exp\left(k_f SF_j\right)}{\sum_{i \in \Omega_i} \exp\left(k_f SF_i\right)}
$$

where $k_f$ represents the pedestrian’s familiarity with the exit, and a constant 10 is used in this paper. $\Omega_i$ represents the set of all accessible grids near pedestrian i.

## 3.1 Evacuation of Pedestrian Conflict Game

In the simulation, this paper uses the parallel update rule. Conflicts arise when two or more pedestrians intend to move to the same grid at the same time step. When a conflict occurs, the idea of a game is used to solve the problem. Generally, in the face of positional conflict, comity and scramble are common handling methods adopted by pedestrians. The solution rule adopts the typical game model "Prisoner’s Dilemma". In the prisoner’s dilemma game, there are two different strategies, which we define as cooperation (C) and betrayal (D) (cooperation means the strategy of humility, and the pedestrian who adopts this strategy is defined as the cooperator; defection means the strategy of contention, a pedestrian who adopts this strategy is defined as a traitor). Taking a simple two-player game model as an example to illustrate the conflict resolution rules, the payoff matrix of the game is shown in Table 1:

The second row shows the payoff of taking strategy C (cooperation), while the third row shows the payoff of taking strategy D (defection). R is the payoff of the two collaborators. P is the payoff of the two defectors. When one pedestrian adopts the cooperative strategy and the other adopts the defection strategy, the payoff of the cooperator and the defection is (S, T). When T>P>R>S is satisfied, it is a classic prisoner’s dilemma game. This means: (1) when competing with the cooperator, the pedestrian who adopts the defection will get the highest reward; (2) when both adopt the cooperative strategy, both will get a relatively high reward and can withdraw faster out of the room; (3) when competing with defectors, adopting the cooperative strategy will yield very low returns; (4) when competing with defectors, adopting the defecting strategy will obtain relatively low returns, both pedestrians may Unable to move. Based on the consideration of the prisoner’s dilemma game, we transform the payoff matrix into a probability matrix that represents the probability of pedestrian movement in the event of a conflict, where P represents the penalty for defectors. (Sometimes the opportunity to move is lost because the pedestrian is too conflicted).

#### Table 1: Two-Player Game Payoff Matrix

|     | C   | D   |
| --- | --- | --- |
| C   | R   | S   |
| D   | T   | P   |

#### Table 2: Two-Player Conflict Game Matrix

|     | C     | D       |
| --- | ----- | ------- |
| C   | $1/2$ | $0$     |
| D   | $1$   | $1/2^P$ |

#### Table 3: Multi-Player Conflict Game Matrix

|     | $(M-1)C, 0D$ | $MC, (N-M-1)$ |
| --- | ------------ | ------------- |
| C   | $1/M$        | $0$           |
| D   | $1$          | $1/(N-M)^P$   |

In our study, each pedestrian may compete with their neighbors within the Moore neighborhood. Then, the number of participants in the conflict may be greater than 2, which means that the two player game rules can be extended to multi-player games, as shown in Table 3 below.

For the case where the number of conflicts is greater than 2, the number of conflicts is set to N, and the number of collaborators is set to M. When M=N,the pedestrians in the conflict enter the target with an equal probability of 1/M. If there is only one defector, that is, $N-M=1$, the defector directly enters the target. If the defector is greater than 1, that is, N-M>1, the defector will enter the target with the probability $1/(N − M)P$ goes to the goal. Through the study of previous literature, 1 ≥ $P$ ≥ 2.5 is considered in this paper.

## 3.2 Policy Update

In the game, pedestrians who fail to enter the target will change their strategy, that is, update the strategy according to the corresponding rules. When the pedestrian updates the strategy, it will estimate the return of comparing the current strategy and the opposite strategy. Usually, due to inertia, pedestrians tend to maintain the current strategy, but when the income gap is relatively large, pedestrians will change the current strategy. In order to describe this phenomenon, $U_i$ and $U_j$ are set as the income obtained by pedestrians in the actual game, and d represents inertia. It is assumed that pedestrians will overestimate the income brought by the current strategy in the process of updating their strategies.

$$M_x = d * U_i; (\beta > 1)$$

$$M_y = U_j$$

$Mx$ represents the estimated payoff of the current policy when pedestrians update the policy, and $Mx$ estimates the payoff of the opposite policy. In each cycle $c$, if the pedestrian game fails, the pedestrian will update his strategy by changing to the opposite strategy learning with probability $W (Sx -Sy)$ . The article updates the pedestrian’s own policy according to the Fermi function:

$$W_{(s_x, -s_y)} = \frac{1}{1 + \exp\left[\frac{M_x - M_y}{k}\right]}$$

where $Sx$ represents the current policy, $Sy$ represents the opposite policy, $k$ represents noise, which represents the strength of irrationality, without loss of generality, we set $k$ to 0.1.

## 4 EXPERIMENTS

The main hardware environment of the experiment is NVIDIA RTX 2070S GPU, 16G memory, Intel i7-10700K CPU, and the software environment is WIN10system, Matlab software, and unity platform.

### 4.1 Update Strategy Experiments

#### 4.1.1 Effects of Update Cycle

First, let’s explore the impact of the strategy update period. It can be observed from Figure 1(a) that when the update period is set to different values, the larger the proportion of the number of people who cooperate, the shorter the evacuation time; when the update period is smaller, 1, 5 and 10, that is, when the frequency of pedestrian update strategy is more frequent, when the ratio of cooperators increases from 0.1 to 0.5, the evacuation time decreases with the increase of $RC$ much less than when the evacuation time increases from 0.5 to 0.9. increase and decrease. This is due to the fact that when $RC$ is slightly less than 0.5, the betrayer dominates, and the cooperators in the room cannot move and change their strategies when they conflict with many betrayers, thus increasing the possibility of pedestrians updating to the betraying strategy, and at this time the pedestrians Frequent updating of the strategy leads to more and more defectors. Because the defectors are more likely to be pushed and unable to move, the evacuation time becomes longer. Therefore, when $RC$ is less than 0.5, the effect of increasing initial partners on evacuation time is not significant, and when $RC$ is greater than 0.5, the cooperator is dominant, and most of the conflicts are between cooperators, and the cooperators can win their own goals in the conflict, so the possibility of the pedestrian’s strategy changing to the defector is reduced. When the evacuation time is relatively short, increasing the number of partners has a more significant effect on the evacuation time. When the update period is increased to 50, the update frequency of pedestrians is extremely low, and the curve of evacuation time with $RC$ gradually tends to be linear.

When the update period $c$ increases from 1 to 10, the difference between the evacuation time curves is not obvious. When it increases to 50, it can be seen that there is a significant downward shift in the evacuation time curve, especially when $RC$=0.5, the decline is particularly obvious; when $RC$ is around 0.1 or 0.9, the downward trend of the curve is relatively insignificant. This is due to the too strong dominance of cooperators or defectors, and fewer pedestrians take the opposite strategy. The phenomenon is very similar to herd behavior. The above phenomenon is more prominent in Figure 1(b). When $RC$=0.5, it can be intuitively observed that the evacuation time decreases with the increase of the update period, and the change of evacuation time gradually stabilizes until $c$ is greater than 50. When $RC$=0.1 or 0.9, the evacuation time did not fluctuate significantly with the update period.

To intuitively understand the effect of the update period on evacuation, $RC$ is set to 0.4, 0.5, and 0.6 to study the changes in the number of pedestrians with different strategies in the room at different update periods. It can be seen from Figure 2 that when the frequency of pedestrian update strategy is high, the number of defectors in the room has a significant upward trend over time, and the gap between the number of cooperators and defectors in the room will increase during evacuation. It becomes larger and larger over a period, which indicates that there are many situations in which pedestrian strategies change from cooperation to betrayal, especially when the number of defectors and cooperators in the room is equal or the number of defectors is slightly less than that of cooperators, as shown in Figure 2 In the case of (a) and (b), when $RC$ is 0.4 or 0.5, it can be observed that there are many pedestrians whose strategies change from cooperation to defection, because at this time, the cooperators are repeatedly frustrated when competing with the defectors, which leads them to change their strategies; During the evacuation process, the rate of decline in the number of defectors is greater than that of the cooperators, indicating that the defectors can leave the room faster than the cooperators. Therefore, pedestrians generally prefer the betrayal strategy, but the above analysis shows that the defectors The more it is, the longer the evacuation time will be, thus forming the prisoner’s dilemma situation; when c=30, the frequency of pedestrian update strategy is lower, although the number of defectors in the room also has an upward trend, the increase is greatly reduced.

#### 4.1.2 Effects of Inertia

Set the update period c to 5 and the traitor penalty P to 2. As can be seen from Figure 3, in most cases, the greater the inertia, the shorter the evacuation time. In Figure 3(a), when the inertia d increases from 1 to 2, the evacuation time is very close under different $RC$ due to the small change in inertia. Shifting downward, when $RC$ is around 0.5, the magnitude of the downward shift of evacuation time is relatively large, while when $RC$ is around 0.1 and 0.9, the magnitude of the shift is relatively small. This phenomenon can also be verified in Figure 3(b), when $RC$=0.5, it can be observed that the histogram has a significant downward trend with the increase of d, and there is no obvious change trend when $RC$=0.1 and 0.9, When the inertia d increases to about 5, increasing the inertia has little effect on the evacuation time.

In the simulation analysis, c=5, and when the value of d is small, that is, the pedestrian strategy is updated more frequently, and the slope of the evacuation time versus the $RC$ curve is gentle before 0.5, and gradually becomes steeper after $RC$ is set to 0.5. When d gradually becomes larger, the possibility of pedestrian update strategy gradually becomes smaller, and the curve of evacuation time with $RC$ gradually becomes stable.

It can be found from Figure 4 that when the inertia is large, pedestrians are less likely to update the policy, and even the policy update will be frozen. Compared with d=1, when d=4, the transformation of pedestrians from collaborators to defectors is significantly suppressed. Especially when $RC$=0.5, it can be observed in Figure 4(b) that when the inertia is small, it can be seen that the number of defectors in the room rises sharply after the evacuation is carried out for a period of time, while when the inertia is large, the number of defectors in the room increases sharply The number is steadily decreasing. Similar situations are reflected when $RC$ is 0.4 and 0.6.

#### 4.1.3 Effects of Betrayer Punishment

The most obvious difference is when $RC$ is less than 0.5. In Figure 5(a), the curve of evacuation time versus $RC$ has a very gentle downward trend. The reason for this is that pedestrians frequently update the strategy. Whether the pedestrian adopts the update or no update strategy, punishing P will have an adverse effect when there are many defectors in the room.

It can be seen from Figure 6 that when P=1.0 is compared with P=2.5, when P=2.5, the possibility of pedestrians changing from cooperators to defectors is less, and the larger P is, the longer the evacuation time will be. The effect of P on the pedestrian policy update is not as obvious as the effect of inertia. Overall, pedestrians are more inclined to choose the betrayal strategy, resulting in a prisoner’s dilemma situation. Inertia, punishment for betrayers, and update cycles are mostly inhibiting the transition from cooperators to betrayers.

### 4.2 Simulation Experiments

#### 4.2.1 Parameter Setting

The gymnasium covers an area of 20m \* 20m. The field consists of the side fence, the competition field, and the spectator seats. Among them, the field side guardrail is 2.3m high, there are four passage exits at the four corners of the guardrail, and the audience seats surround the competition area. The plan structure of the stadium is shown in Figure 7.

The gymnasium has evacuation exits 1, 2, 3, and 4, each with a width of 1.2m. The length of each side guardrail is 12.4m, and the width of one side of the passage exit at the four corners of the guardrail is 0.8m. Divide the gymnasium plane into 50 * 50 grids, and each grid is 0.4m*0.4m. A cell has three states: occupied by pedestrians, occupied by obstacles, and empty. The 2.3m guardrails is the main obstacle in the field, and pedestrians cannot cross this obstacle.

The simulation model of the gymnasium is shown in Figure 8 below.

#### 4.2.2 PersonnelEvacuationProcess

First, quantify the environmental information of the gymnasium and related system requirements through quantitative analysis, then set the personnel attribute parameters, and finally establish a motion simulation model and a behavioral decision-making model. The specific implementation steps are:

1. Enter the environmental information of the gymnasium in the MATLAB platform, including the area layout: the length of the museum is 20m and the width of 20m; the exit position: there are four exits, which are distributed on both sides of the two opposite walls. Guardrail location: Four 12.4m-long guardrails divide the playing field into a 13m\*13m square area. Audience seat location: neatly arranged near the four walls.
2. The attribute setting of pedestrians when an emergency occurs, the radius of pedestrians is set to 0.2m, and the speed of pedestrians is set to 1.65m/s. In the simulation in this chapter, the pedestrian’s exit selection inertia is set to 0.2, the conflict game strategy and update period are set to 5, the penalty for defectors is set to 2, and the conflict strategy inertia is set to 2.
3. At each time step, evacuate the room according to the following rules.

For the personnel inside the guardrail, their primary goal is to evacuate from the arena, and their current exit selection strategy set is the four exits at the corner of the arena; for the personnel inside the stadium outside the guardrail, their goal is to evacuate from the stadium, and they exit at this time. The selected strategy set is exit 1, 2, 3, and 4, and then select the appropriate exit according to the exit selection game rules in Chapter 3.

When two or more pedestrians compete for the position, the conflict strategy of the current time step is selected according to the conflict game rules in Chapter 5, and then the pedestrians entering the target cell are determined.

Update the positions of all pedestrians in parallel.

Repeat steps (1) to (3) until all pedestrians are evacuated from the room.

#### 4.2.3 Simulation Result

1. **Crowd Evacuation in Sports Venues Held in Stadiums:**
   At the initial moment, when T=0, there are 5 rows of 35 seats in the auditorium. Suppose there are 700 spectators and 150 spectators are randomly distributed in the stadium. Therefore, there are a total of 850 evacuees in the stadium at this time, which is relatively dense. Figure 9 simulates the situation where the initial collaborator ratio is 50% and the field of view radius R is 3m. Observing Figure 9, it can be seen that the proportion of defectors in the evacuation is higher and higher over time, relative to the cooperators, the proportion of defectors gathered near the exit is larger, and they can leave the room more quickly. Figure 11 simulates the situation where the initial collaborator ratio is 90% and the field of view radius is 10m. Comparing Figure 11 and Figure 9 at T=140, there are fewer people in the room in Figure 11 who did not leave the room, and the final evacuation time is 160-time steps, while the final evacuation time for the situation shown in Figure 9 is 189-time steps, indicating that cooperative behavior is beneficial to the entire evacuation process.

2. **Crowd Evacuation in the Rehearsal Scene in the Gymnasium:** Assuming that there are 20\*20 or 400 people in the current stadium, they will gather together for some kind of collective activity, and 20 idle personnel or commanders will be randomly distributed in the stadium. Figure 13 simulates the situation where the initial cooperation ratio is 50% and the field of view radius is 3m. Figure 15 simulates the situation where the initial collaborator ratio is 90% and the field of view radius is 10m. Comparing the two figures, we can find that when T=70, the proportion of people who choose each exit in Figure 15 is more uniform, while Figure 13 shows that the proportion of people who choose each exit is not uniform. Large; when T=140, the people in the hall in Figure 15 have basically been evacuated, and Figure 13 shows that there is still a large part of the people who have not evacuated from the room. By comparing the evacuation efficiency under different crowd parameters, it can be known that under the setting scene of $RC=0.9$ and $R=10$, the crowd evacuation effect is better, which shows that in the same scene, a bright and clear vision can improve crowd evacuation At the same time, the mutual cooperation between the crowds can also ensure that the evacuation process is completed more efficiently to a certain extent.

#### 4.2.4 Evaluation of Simulation Results

For the evaluation of the simulation results, a user survey is used to verify the similarity between the simulation results of the model and the real scene. The goal of the users participating in the survey is to objectively compare the similarity between the simulation results of the model and the real scene, and according to the degree of similarity in appearance, the comparison pictures of the above four groups of simulation results and the real scene are classified as "especially similar" and "generally similar" and "dissimilar" on 3 scales

Figure 17 shows the results of the user survey. For the four sets of simulation graphs shown in Figure 10, Figure 12, Figure 14, and Figure 16, the 30 users who participated in the survey gave an overall "particularly similar" ratio of 88.6%, and a "generally similar" ratio of 88.6%. is 6.54%, and the “dissimilar” ratio is 4.86%, indicating that the game theory-based model proposed in this chapter has high fidelity in simulating the crowd evacuation process in stadiums.

## 5 CONCLUSION

The purpose of this paper is to explore the behavioral decision of pedestrians in crowd evacuation based on game theory from the behavioral characteristics of pedestrians. The main work of this paper is as follows. (1) We propose a crowd evacuation model incorporating cellular automata and game theory. (2) We introduce penalty factors and inertia indices in the model based on game theory and formulate the game rules for pedestrian location conflicts. (3) We compare the effect of pedestrians adopting an update and non-update strategy on crowd evacuation in our experiments and simulate the model in a sports scenario.

Based on the above work, we found that the higher the proportion of initial cooperators and the larger the radius of view, the shorter the time for crowd evacuation. Therefore, keeping the building interior brightly lit and properly educating the entering pedestrians can improve crowd evacuation efficiency. All individuals in this paper are considered rational individuals who comply with the model’s behavioral decisions. However, in real emergencies, the crowd’s composition is complex, and the factors affecting their decision-making are diverse. In future work, our research direction can introduce more decision strategies and influencing factors into the model to construct a more realistic crowd evacuation model.

## ACKNOWLEDGMENTS

We are grateful for the support of the research group during this research work.
