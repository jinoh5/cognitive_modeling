# cognitive_modeling

Built by Jin Oh (yu.jin.oh84@gmail.com)

Input: Choice datasets of mice performing a dynamic two-armed bandit task

In this code, I have not added the mice choice dataset for privacy issue. If needed, please contact the author.

Output:
- Qualitative diagnostics of average mice behavior
- Qualitative diagnostics of agents' behavior
- Quantitative comparison between synthetic agents (cross-validated normalized log likliehood scores)

[Supplementary Information]
- Generative agents: vanillaQ_agent, optimisticQ_agent, generalized_local_matching_law_agent, forgettingQ_agent, differential_forgettingQ_agent, habitsRL_agent, basic_ideal_observer_agent, ideal_observer_1_back_perseveration_agent, ideal_observer_habits_agent, marginal_value_theorem_agent
- Qualitative diagnostics:
   - Trial history generalized linear models (choice perseveration, reward seeking, main effect of reward)
   - Choice Bias
   - Bout distribution
   - Learning curve
- Modeling fitting software: Pystan
