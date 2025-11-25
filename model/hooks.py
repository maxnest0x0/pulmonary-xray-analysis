class ActivationHook:
    """
    Обёртка forward-hook:
    при проходе через слой сохраняет feature maps.
    """
    def __init__(self, module):
        self.module = module
        self.handle = module.register_forward_hook(self._hook_fn)
        self.output = None

    def _hook_fn(self, module, input, output):
        self.output = output.detach().cpu()

    def remove(self):
        self.handle.remove()

class GradientHook:
    """
    Обёртка над backward-hook:
    при обратном проходе сохраняет градиенты по выходу слоя.
    """
    def __init__(self, module):
        self.module = module
        self.handle = module.register_full_backward_hook(self._hook_fn)
        self.grad = None

    def _hook_fn(self, module, grad_input, grad_output):
        self.grad = grad_output[0].detach().cpu()

    def remove(self):
        self.handle.remove()