# -*- coding: utf-8 -*-
"""fit_functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XiesHllu7nM4c5j4MNok8h24uKQSZYDD
"""

#pip install pystan

import pystan

vanillaQ_model ="""
data {

    int<lower=0> nTrials;
    int nSession;
    int session_index[nSession];
    int<lower=0,upper=1> choices[nTrials];
    int<lower=0,upper=1> rewards[nTrials];

}

parameters {

    real<lower=0,upper=1> learning_rate;
    real decision_noise;
    real beta_bias;

}

transformed parameters {

    real loglikelihood;
    {
      vector[2] Q;

      Q[1]=0.5; Q[2]=0.5; loglikelihood=0;
      
      for (trial_i in 1:nTrials) {
        for (session_i in 1:nSession) { 
          if (trial_i == session_i) {
            Q[1] = 0.5;  //new_session set up
            Q[2] = 0.5;
          }
        }
        Q[1] = Q[1]+beta_bias;
        Q[2] = Q[2]-beta_bias;
        loglikelihood += categorical_lpmf((choices[trial_i]+1) | softmax(decision_noise * Q));      
        Q[choices[trial_i]+1] = Q[choices[trial_i]+1] * (1-learning_rate)+ learning_rate * rewards[trial_i];
      }
    }  
}

model {

    // Priors for parameters
    target += normal_lpdf(decision_noise| 0, 10);
    target += beta_lpdf(learning_rate| 2, 2);
    target += normal_lpdf(beta_bias|0, 10);
    target += loglikelihood;

}
"""

optimisticQ_model= """
data {

    int<lower=0> nTrials;
    int nSession;
    int session_index[nSession];
    int<lower=0,upper=1> choices[nTrials];
    int<lower=0,upper=1> rewards[nTrials];

}

parameters {

    real<lower=0,upper=1> learning_rate_pos;
    real<lower=0,upper=1> learning_rate_neg;
    real decision_noise;
    real beta_bias;

}

transformed parameters {

    real loglikelihood;
      // Define a helper variable Q
      { 
      vector[2] Q;
      
      // Assign initial values to Q
      Q[1]=0.5; Q[2]=0.5; loglikelihood=0;

      // Draw each trial's data, using the observed choices and rewards, as well as the parameters

      for (trial_i in 1:nTrials) {
        for (session_i in 1:nSession) {
          if (trial_i == session_i) {
            Q[1] = 0.5;
            Q[2] = 0.5;
          }
        }
        Q[1] = Q[1]+beta_bias;
        Q[2] = Q[2]-beta_bias;
        loglikelihood += categorical_lpmf((choices[trial_i]+1) | softmax(decision_noise * Q));
        
        if (rewards[trial_i]==1) {
          Q[choices[trial_i]+1] = Q[choices[trial_i]+1] * (1-learning_rate_pos) + learning_rate_pos * rewards[trial_i];
        } 
        else {
          Q[choices[trial_i]+1] = Q[choices[trial_i]+1] * (1-learning_rate_neg) + learning_rate_neg * rewards[trial_i];
        }
      }
    }
}

model {
    
    // Priors for parameters
    target += normal_lpdf(decision_noise| 0, 10);
    target += beta_lpdf(learning_rate_pos| 2, 2);
    target += beta_lpdf(learning_rate_neg| 2, 2);
    target += normal_lpdf(beta_bias|0, 10);
    target += loglikelihood;
    
  }
"""

generalized_local_matching_law_model = """
data {

    int nTrials;
    int nSession;
    int session_index[nSession];
    int choices[nTrials];
    int rewards[nTrials];

}

parameters {

    real <lower=0, upper=1> learning_rate;
    real <lower=0> sensitivity;
    real <lower=0> bias;

}
transformed parameters {

    real loglikelihood;

      {
      vector[2] Q;
      Q[1] = 0.5; Q[2] = 0.5; loglikelihood = 0;
      
      for (trial_i in 1:nTrials) {
        for (session_i in 1:nSession) {
          if (trial_i == session_i) {
            Q[1] = 0.5;
            Q[2] = 0.5;
          }
        }
        
        loglikelihood += bernoulli_lpmf((choices[trial_i])| bias*(pow(Q[2]/(Q[1]+Q[2]), sensitivity)));
        
        if (choices[trial_i]==0 && rewards[trial_i]==1) {
          Q[1] = (1-learning_rate)*Q[1]+learning_rate;
          Q[2] = (1-learning_rate)*Q[2];
        } 
        else if (choices[trial_i]==1 && rewards[trial_i]==1) {
          Q[1] = (1-learning_rate)*Q[1];
          Q[2] = (1-learning_rate)*Q[2]+learning_rate;
        } 
        else {
          Q[1] = (1-learning_rate)*Q[1];
          Q[2] = (1-learning_rate)*Q[2];
        }
      }
    }
}
model {

    // Priors for parameters
    target += beta_lpdf(learning_rate| 2, 2);
    target += normal_lpdf(sensitivity| 0, 10);
    target += normal_lpdf(bias| 0, 10);
    target += loglikelihood;

}
"""

forgettingQ_model = """
data {

    int<lower=0> nTrials;
    int nSession;
    int session_index[nSession];
    int<lower=0,upper=1> choices[nTrials];
    int<lower=0,upper=1> rewards[nTrials];
}

parameters {

    real <lower=0,upper=1> learning_rate;
    real <lower=0> reward_strength;
    real <lower=0> aversion_strength;
    real beta_bias;
}
transformed parameters {

    real loglikelihood;
      // Define a helper variable Q
      { 
      vector[2] Q;
      
      // Assign initial values to Q
      Q[1] = 0.5; Q[2] = 0.5; loglikelihood = 0;

      // Draw each trial's data, using the observed choices and rewards, as well as the parameters

      for (trial_i in 1:nTrials) {
        for (session_i in 1:nSession) {
          if (trial_i == session_i) {
            Q[1] = 0.5;
            Q[2] = 0.5;
          }
        }
        Q[1] = Q[1]+beta_bias;
        Q[2] = Q[2]-beta_bias;
        loglikelihood += categorical_lpmf((choices[trial_i]+1) | softmax(Q));

        if (choices[trial_i]==0 && rewards[trial_i]==1) {
          Q[1] = (1-learning_rate)*Q[1]+learning_rate*reward_strength;
          Q[2] = (1-learning_rate)*Q[2];
        } 
        else if (choices[trial_i]==0 && rewards[trial_i]==0) {
          Q[1] = (1-learning_rate)*Q[1]-learning_rate*aversion_strength;
          Q[2] = (1-learning_rate)*Q[2];
        } 
        else if (choices[trial_i]==1 && rewards[trial_i]==1) {
          Q[1] = (1-learning_rate)*Q[1];
          Q[2] = (1-learning_rate)*Q[2]+learning_rate*reward_strength;
        } 
        else if (choices[trial_i]==1 && rewards[trial_i]==0) {
          Q[1] = (1-learning_rate)*Q[1];
          Q[2] = (1-learning_rate)*Q[2]-learning_rate*aversion_strength;
        }
      }
    } 
  }
model {

    // Priors for parameters
    target += beta_lpdf(learning_rate| 2, 2);
    target += normal_lpdf(reward_strength|0, 10);
    target += normal_lpdf(aversion_strength|0, 10);
    target += normal_lpdf(beta_bias|0, 10);
    target += loglikelihood; 

  }
"""

differential_forgettingQ_model = """
data {

    int<lower=0> nTrials;
    int nSession;
    int session_index[nSession];
    int<lower=0,upper=1> choices[nTrials];
    int<lower=0,upper=1> rewards[nTrials];
}

parameters {

    real <lower=0,upper=1> learning_rate;
    real <lower=0,upper=1> forgetting_rate;
    real reward_strength;
    real aversion_strength;
    real beta_bias;
}

transformed parameters {

    real loglikelihood;
      { 
      vector[2] Q;
      
      Q[1] = 0.5; Q[2] = 0.5; loglikelihood = 0;

      for (trial_i in 1:nTrials) {
        for (session_i in 1:nSession) {
          if (trial_i == session_i) {
            Q[1] = 0.5;
            Q[2] = 0.5;
          }
        }
        Q[1] = Q[1]+beta_bias;
        Q[2] = Q[2]-beta_bias;
        loglikelihood += categorical_lpmf((choices[trial_i]+1) | softmax(Q));

        if (choices[trial_i]==0 && rewards[trial_i]==1) {
          Q[1] = (1-learning_rate)*Q[1]+learning_rate*reward_strength;
          Q[2] = (1-forgetting_rate)*Q[2];
      } 
        else if (choices[trial_i]==0 && rewards[trial_i]==0) {
          Q[1] = (1-learning_rate)*Q[1]-learning_rate*aversion_strength;
          Q[2] = (1-forgetting_rate)*Q[2];
      } 
        else if (choices[trial_i]==1 && rewards[trial_i]==1) {
          Q[1] = (1-forgetting_rate)*Q[1];
          Q[2] = (1-learning_rate)*Q[2]+learning_rate*reward_strength;
      } 
        else if (choices[trial_i]==1 && rewards[trial_i]==0) {
          Q[1] = (1-forgetting_rate)*Q[1];
          Q[2] = (1-learning_rate)*Q[2]-learning_rate*aversion_strength;

        }
      }
    } 
  }

model {

    // Priors for parameters
    target += beta_lpdf(learning_rate| 2, 2);
    target += beta_lpdf(forgetting_rate| 2, 2);
    target += normal_lpdf(reward_strength|0, 10);
    target += normal_lpdf(aversion_strength|0, 10);
    target += normal_lpdf(beta_bias|0, 10);
    target += loglikelihood;

}
"""

habitsRL_model="""
data {

  int<lower=0> nTrials;
  int nSession;
  int session_index[nSession];
  int<lower=0,upper=1> choices[nTrials];
  int<lower=0,upper=1> rewards[nTrials];

}

parameters {

  real<lower=0, upper=1> alpha_rl;
  real<lower=0, upper=1> alpha_habit;
  real beta_rl;
  real beta_habit;
  real beta_bias;

}

transformed parameters {

  real loglikelihood;
  {
    real Q; real H; real decision_variable;
    int choice_for_update; int reward_for_update; 
    Q = 0.5; H = 0; loglikelihood = 0; 

    for (trial_i in 1:nTrials) {
      for (session_i in 1:nSession) {
        if (trial_i == session_i) {
          Q = 0.5;
          H = 0;
        }
      }

      // Update the internal decision variable 
      decision_variable = beta_rl * Q + beta_habit * H + beta_bias;
      loglikelihood += bernoulli_lpmf((choices[trial_i]) | 1/(1+exp(-1*decision_variable)));

      // Convert choice and reward from 0, 1 to -1, +1 
      choice_for_update = 2*choices[trial_i] - 1;
      reward_for_update = 2*rewards[trial_i] - 1;

      Q = Q * (1-alpha_rl) + alpha_rl * choice_for_update * reward_for_update;
      H = H * (1-alpha_habit) + alpha_habit * choice_for_update;
    }
  }
}

model {
  target += beta_lpdf(alpha_rl| 2, 2);
  target += normal_lpdf(beta_rl|0, 10);
  target += beta_lpdf(alpha_habit|2, 2);
  target += normal_lpdf(beta_habit|0, 10);
  target += normal_lpdf(beta_bias|0, 10);
  target += loglikelihood;
}
"""

basic_ideal_observer_model = """
data {
  int<lower=0> nTrials;
  int nSession;
  int session_index[nSession];
  int<lower=0,upper=1> choices[nTrials];
  int<lower=0,upper=1> rewards[nTrials];
}
parameters {
  real beta_v;
  real beta_bias;
}
transformed parameters {

  real loglikelihood;
  {
    real Q_left; 
    real Q_right; 
    int choice_for_update;
    int reward_for_update;
    real decision_variable;
    real p_observation_given_left_better; 
    real p_observation_given_right_better;
    real p_observation; 
    real belief_after_bayes_update; 
    real belief_after_dynamics_update;
    real belief_left_better;

    belief_left_better=0.5; loglikelihood=0;

    for (trial_i in 1:nTrials) {
      for (session_i in 1:nSession) {
        if (trial_i == session_i) {
          belief_left_better = 0.5;
        }
      }

      // Update the Q internal variable 
      Q_left = 0.8 * belief_left_better + 0.2 * (1-belief_left_better);
      Q_right = 0.8 * (1-belief_left_better) + 0.2 * belief_left_better;

      // Get choice 
      decision_variable = beta_v * (Q_right-Q_left) + beta_bias;
      loglikelihood += bernoulli_lpmf((choices[trial_i]) | 1/(1+exp(-1*decision_variable)));

      // Convert choice and reward from 0, 1 to -1, +1 
      choice_for_update = 2*choices[trial_i] - 1;
      reward_for_update = 2*rewards[trial_i] - 1;

      // Bayesian update
      if (choice_for_update == -1 && reward_for_update == -1) {
        p_observation_given_left_better = 0.2;
        p_observation_given_right_better = 0.8;
      }
      else if (choice_for_update == -1 && reward_for_update == 1) {
        p_observation_given_left_better = 0.8;
        p_observation_given_right_better = 0.2;
      }
      else if (choice_for_update == 1 && reward_for_update == -1) {
        p_observation_given_left_better = 0.8;
        p_observation_given_right_better = 0.2;
      }
      else if (choice_for_update == 1 && reward_for_update == 1) {
        p_observation_given_left_better = 0.2;
        p_observation_given_right_better = 0.8;
      }
      // Compute p(observation)
      p_observation = belief_left_better * p_observation_given_left_better + (1-belief_left_better) * p_observation_given_right_better;
      
      // Bayes Theorem update (posterior = prior x likelihood)
      belief_after_bayes_update = belief_left_better * p_observation_given_left_better / p_observation;
      
      // Dynamics update
      belief_after_dynamics_update = belief_after_bayes_update * (1 - 0.02) + (1 - belief_after_bayes_update) * 0.02;
      
      // Set the belief property
      belief_left_better = belief_after_dynamics_update;
    }
  }
}

model {
  target += normal_lpdf(beta_v |0, 10);
  target += normal_lpdf(beta_bias |0, 10);
  target += loglikelihood;
}
"""

ideal_observer_1_back_perserveration_model = """
data {
  int<lower=0> nTrials;
  int nSession;
  int session_index[nSession];
  int<lower=0,upper=1> choices[nTrials];
  int<lower=0,upper=1> rewards[nTrials];
}
parameters {
  real beta_v;
  real beta_bias;
  real beta_perserv;
}
transformed parameters {

  real loglikelihood;
  {
    real Q_left;
    real Q_right;
    int choice_for_update;
    int reward_for_update;
    real decision_variable;
    real p_observation_given_left_better; 
    real p_observation_given_right_better;
    real p_observation; 
    real belief_after_bayes_update; 
    real belief_after_dynamics_update;
    real belief_left_better;
    int previous_choice; 

    belief_left_better = 0.5; previous_choice = -1; 
    loglikelihood=0;
    
    for (trial_i in 1:nTrials) {
      for (session_i in 1:nSession) {
        if (trial_i == session_i) {
          belief_left_better = 0.5;
        }
      }
      Q_left = 0.8 * belief_left_better + 0.2 * (1-belief_left_better);
      Q_right = 0.8 * (1-belief_left_better) + 0.2 * belief_left_better;

      decision_variable = beta_v * (Q_right-Q_left) + beta_bias + beta_perserv * previous_choice;
      loglikelihood += bernoulli_lpmf((choices[trial_i]) | 1/(1+exp(-1*decision_variable)));
      
      // Convert choice and reward from 0, 1 to -1, +1 
      choice_for_update = 2*choices[trial_i] -1;
      reward_for_update = 2*rewards[trial_i] -1;

      // Update the 1-back previous choice 
      previous_choice = choice_for_update;

      // Bayesian update
      if (choice_for_update == -1 && reward_for_update == -1) {
        p_observation_given_left_better = 0.2;
        p_observation_given_right_better = 0.8;
      }
      else if (choice_for_update == -1 && reward_for_update == 1) {
        p_observation_given_left_better = 0.8;
        p_observation_given_right_better = 0.2;
      }
      else if (choice_for_update == 1 && reward_for_update == -1) {
        p_observation_given_left_better = 0.8;
        p_observation_given_right_better = 0.2;
      }
      else if (choice_for_update == 1 && reward_for_update == 1) {
        p_observation_given_left_better = 0.2;
        p_observation_given_right_better = 0.8;
      }

      // Compute p(observation)
      p_observation = belief_left_better * p_observation_given_left_better + (1-belief_left_better) * p_observation_given_right_better;
      
      // Bayes Theorem update (posterior = prior x likelihood)
      belief_after_bayes_update = belief_left_better * p_observation_given_left_better / p_observation;
      
      // Dynamics update
      belief_after_dynamics_update = belief_after_bayes_update * (1 - 0.02) + (1 - belief_after_bayes_update) * 0.02;
      
      // Set the belief property
      belief_left_better = belief_after_dynamics_update;
    }
  }
}

model {
  target += normal_lpdf(beta_v |0, 10);
  target += normal_lpdf(beta_bias |0, 10);
  target += normal_lpdf(beta_perserv |0, 10);
  target += loglikelihood;
}
"""

ideal_observer_habits_model = """
data {
  int<lower=0> nTrials;
  int nSession;
  int session_index[nSession];
  int<lower=0,upper=1> choices[nTrials];
  int<lower=0,upper=1> rewards[nTrials];
}
parameters {
  real beta_v;
  real beta_habit;
  real alpha_habit;
  real beta_bias;
}
transformed parameters {

  real loglikelihood;
  {
    real Q_left;
    real Q_right;
    int choice_for_update;
    int reward_for_update;
    real decision_variable;
    real p_observation_given_left_better;
    real p_observation_given_right_better;
    real p_observation;
    real belief_after_bayes_update;
    real belief_after_dynamics_update;
    real belief_left_better;
    real h; 

    belief_left_better = 0.5; h = 0; 
    loglikelihood = 0;

    for (trial_i in 1:nTrials) {
      for (session_i in 1:nSession) {
        if (trial_i == session_i) {
          belief_left_better = 0.5;
          h = 0;
        }
      }
      Q_left = 0.8 * belief_left_better + 0.2 * (1-belief_left_better);
      Q_right = 0.8 * (1-belief_left_better) + 0.2 * belief_left_better;

      decision_variable = beta_v * (Q_right-Q_left) + beta_habit * h + beta_bias; 
      loglikelihood += bernoulli_lpmf((choices[trial_i]) | 1/(1+exp(-1*decision_variable)));

      // Convert choice and reward from 0, 1 to -1, +1 
      choice_for_update = 2*choices[trial_i] -1;
      reward_for_update = 2*rewards[trial_i] -1;

      // Bayesian update
      if (choice_for_update == -1 && reward_for_update == -1) {
        p_observation_given_left_better = 0.2;
        p_observation_given_right_better = 0.8;
      }
      else if (choice_for_update == -1 && reward_for_update == 1) {
        p_observation_given_left_better = 0.8;
        p_observation_given_right_better = 0.2;
      }
      else if (choice_for_update == 1 && reward_for_update == -1) {
        p_observation_given_left_better = 0.8;
        p_observation_given_right_better = 0.2;
      }
      else if (choice_for_update == 1 && reward_for_update == 1) {
        p_observation_given_left_better = 0.2;
        p_observation_given_right_better = 0.8;
      }
      //Compute p(observation)
      p_observation = belief_left_better * p_observation_given_left_better + (1-belief_left_better) * p_observation_given_right_better;
      
      // Bayes Theorem update: Posterior = prior * likelihood
      belief_after_bayes_update = belief_left_better * p_observation_given_left_better / p_observation;
      
      // Dyanmics update
      belief_after_dynamics_update = belief_after_bayes_update * (1 - 0.02) + (1 - belief_after_bayes_update) * 0.02;
      
      // Set the belief property
      belief_left_better = belief_after_dynamics_update;
      
      // Update H 
      h = h * (1-alpha_habit) + alpha_habit * choice_for_update;
    }
  }
}

model {
  target += normal_lpdf(beta_v|0, 10);
  target += beta_lpdf(alpha_habit|2, 2);
  target += normal_lpdf(beta_habit|0, 10);
  target += normal_lpdf(beta_bias|0, 10);
  target += loglikelihood;
}
"""
marginal_value_theorem_model = """

data {

    int<lower=0> nTrials;
    int nSession;
    int session_index[nSession];
    int<lower=0,upper=1> choices[nTrials];
    int<lower=0,upper=1> rewards[nTrials];

}

parameters {

    real<lower=0, upper=1> alpha_l;
    real beta;
    real beta_bias;

}

transformed parameters {

    real loglikelihood;
    {
      int previous_choice;
      real local_reward_0;
      real local_reward;
      real general_rate_of_reward;
      real decision_variable;
      real prob_choose_previous;
      real prob_choose_left; 
      real new_local_reward;
      
      local_reward_0 = 0; 
      general_rate_of_reward = 0;
      loglikelihood=0;
      
      for (trial_i in 1:nTrials) {
        for (session_i in 1:nSession) {
          if (trial_i == session_i) {
            previous_choice = 0;
            local_reward = 0.5;
            general_rate_of_reward = 0;
          }
        }
        
        // Get Choice 
        decision_variable = ((local_reward - general_rate_of_reward)/beta)+beta_bias; 
        prob_choose_previous = 1/(1+exp(-2*decision_variable));
        if (previous_choice == 0) {
          prob_choose_left = prob_choose_previous;
        }
        else {
          prob_choose_left = 1 - prob_choose_previous;
        }
        loglikelihood += bernoulli_lpmf(choices[trial_i] | prob_choose_left);
        
        
        // Update 
        new_local_reward = alpha_l * local_reward + (1-alpha_l) * rewards[trial_i];
        if (choices[trial_i] != previous_choice){
          local_reward = local_reward_0;
        }
        else {
          local_reward = new_local_reward;
        }
        previous_choice = choices[trial_i];
      }
    }  
}

model {

    // Priors for parameters
    target += beta_lpdf(alpha_l | 2, 2);
    target += normal_lpdf(beta | 0, 10);
    target += normal_lpdf(beta_bias | 0, 10);
    target += loglikelihood;

}
"""
models = [vanillaQ_model, 
          optimisticQ_model,
          generalized_local_matching_law_model, 
          forgettingQ_model, 
          differential_forgettingQ_model, 
          habitsRL_model,
          basic_ideal_observer_model,
          ideal_observer_1_back_perserveration_model,
          ideal_observer_habits_model,
          marginal_value_theorem_model]