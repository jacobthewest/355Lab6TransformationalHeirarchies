import logging
import moderngl_window as mglw
import numpy as np
from gl_models import House, Car, Tire


class Renderer(mglw.WindowConfig):
    window_size = (512, 512)
    title = "OpenGL Lab"
    gl_version = (3, 3)
    background_color = (0, 0, 0)
    aspect_ratio = 1
    log_level = logging.ERROR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prog = self.ctx.program(vertex_shader="""#version 330 core
layout (location = 0) in vec3 aPos;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1);
}
""", fragment_shader="""#version 330 core
out vec4 FragColor;
uniform vec3 color;

void main() {
    FragColor = vec4(color, 1);
}
""")
        self.house = House(self.ctx, self.prog)
        self.car = Car(self.ctx, self.prog)
        self.tire = Tire(self.ctx, self.prog)
        self.key_pressed = {key: False for key in self.wnd.keys.__dict__.values() if isinstance(key, int)}
        self.keys = self.wnd.keys
        self.model_matrix = []

    def render(self, total_time, delta_time):
        self.ctx.clear(*self.background_color, 1.0)
        self.poll_keys()
        self.prog["projection"].value = tuple(self.get_projection().ravel())
        self.prog["view"].value = tuple(self.get_view().ravel())
        self.render_scene(delta_time)

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            self.key_pressed[key] = True
        if action == self.wnd.keys.ACTION_RELEASE:
            self.key_pressed[key] = False

    def poll_keys(self):
        pass

    def get_projection(self):
        return np.eye(4)

    def get_view(self):
        return np.eye(4)

    def push_model_matrix(self, m):
        self.model_matrix.append(m)

    def pop_model_matrix(self):
        self.model_matrix.pop()

    def get_model_matrix(self):
        model_matrix = np.eye(4)
        for m in self.model_matrix:
            model_matrix = np.matmul(model_matrix, m)
        return model_matrix

    def render_scene(self, delta_time):
        self.house.render(model=np.eye(4), color=np.array([1, 0, 0]))


if __name__ == "__main__":
    Renderer.run()
