import torch
import torch.nn as nn

class Model_1(nn.Module):
    def __init__(self, input_dim, hidden_neurons=[128, 64, 16], output_dim=1, activation=nn.ReLU):
    
        super(Model_1, self).__init__()
        
        layers = []
        in_features = input_dim
        
        for hidden_units in hidden_neurons:
            layers.append(nn.Linear(in_features, hidden_units))
            layers.append(activation())
            in_features = hidden_units

        layers.append(nn.Sigmoid(nn.Linear(in_features, output_dim)))
        
        self.model = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.model(x)