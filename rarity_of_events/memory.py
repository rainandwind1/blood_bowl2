import torch


class Memory(object):
    def __init__(self, num_steps, spatial_obs_shape, non_spatial_shape):
        self.spatial_obs = torch.zeros(num_steps + 1, 1, *spatial_obs_shape)
        self.non_spatial_obs = torch.zeros(num_steps + 1, *non_spatial_shape)
        self.rewards = torch.zeros(num_steps, 1)
        self.value_predictions = torch.zeros(num_steps + 1, 1)
        self.returns = torch.zeros(num_steps + 1, 1)
        action_shape = 1
        self.actions = torch.zeros(num_steps, action_shape)
        self.actions = self.actions.long()
        #self.masks = torch.ones(num_steps + 1, 1)

    def cuda(self):
        self.observations = self.observations.cuda()
        self.rewards = self.rewards.cuda()
        self.value_predictions = self.value_predictions.cuda()
        self.returns = self.returns.cuda()
        self.actions = self.actions.cuda()
       # self.masks = self.masks.cuda()

    def insert(self, step, spatial_obs, non_spatial_obs, action, value_pred, reward):
        self.spatial_obs[step + 1].copy_(spatial_obs)
        self.non_spatial_obs[step + 1].copy_(non_spatial_obs)
        self.actions[step].copy_(action)
        self.value_predictions[step].copy_(value_pred)
        self.rewards[step].copy_(reward)
      #  self.masks[step].copy_(mask)

    def compute_returns(self, next_value, use_gae, gamma, tau=0.1):
        if use_gae:
            self.value_predictions[-1] = next_value
            gae = 0
            for step in reversed(range(self.rewards.size(0))):
                delta = self.rewards[step] + gamma * self.value_predictions[step + 1] * self.masks[step] - self.value_predictions[step]
                gae = delta + gamma * tau * self.masks[step] * gae
                self.returns[step] = gae + self.value_predictions[step]
        else:
            self.returns[-1] = next_value
            for step in reversed(range(self.rewards.size(0))):
                self.returns[step] = self.returns[step + 1] * \
                    gamma + self.rewards[step]
                    # gamma * self.masks[step] + self.rewards[step]