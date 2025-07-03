from autograd.engine import MLP

xs = [[2.0, 3.0, -1.0], [3.0, -1.0, 0.5],
      [0.5, 1.0, 1.0], [1.0, 1.0, -1.0]]

ys = [1.0, -1.0, -1.0, 1.0]

n = MLP(3, [4, 4, 1])

for k in range(41):

    ypred = [n(x) for x in xs]
    loss = sum((ygt - yout)**2 for ygt, yout in zip(ys, ypred))

    # backward pass
    # doing zero grad before backpass
    for p in n.parameters():
        p.grad = 0.0

    loss.backward()

    # update params
    for p in n.parameters():
        p.data -= 0.01 * p.grad

    if k % 5 == 0:
        print(f"Epoch: {k} => Loss: {loss.data}")
