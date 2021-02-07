from FaceNetwork import FaceNetwork
from Dataset import FaceDataset

import torch


def train(net, traindata, device):
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.07)

    for epoch in range(50):
        running_loss = 0
        running_accuracy = 0
        for i, data in enumerate(traindata, 0):
            inputs, labels = data[0].to(device=device, dtype=torch.float), data[1].to(device=device, dtype=torch.long)
            inputs = inputs.permute(0, 3, 1, 2)

            labels = labels.argmax(1)
            outputs = net(inputs)

            loss = criterion(outputs, labels)
            loss.backward()

            total = labels.size(0)
            _, outputs = torch.max(outputs.data, 1)
            correct = (outputs == labels).sum().item()
            running_accuracy += correct / total

            optimizer.step()
            optimizer.zero_grad()

            running_loss += loss.item()

            print(f"Running loss: {running_loss/(i+1):.3f}\tRunning Accuracy: {running_accuracy/(i+1)}", end = '\r')
        print()


if __name__ == "__main__":
    net = FaceNetwork()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net.to(device)

    traindata = FaceDataset("./Data_richard_crop", train = True)
    trainloader = torch.utils.data.DataLoader(traindata, batch_size = 4, shuffle = True, num_workers = 4)

    train(net, trainloader, device)
