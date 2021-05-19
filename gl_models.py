import numpy as np
import moderngl as gl


class RenderObj:
    def __init__(self, ctx: gl.Context, program: gl.Program):
        self.ctx = ctx
        self.program = program
        self.model = np.eye(4)
        verts = self.get_verts()
        vbo = self.ctx.buffer(verts)
        self.vao = self.ctx.simple_vertex_array(self.program, vbo, "aPos")

    def get_verts(self):
        raise NotImplementedError("get_verts needs to be implemented to select the vertices")

    def render(self, model=np.eye(4), color=np.array([1, 0, 0]), mode=gl.LINE_LOOP):
        self.program["model"].value = tuple(model.ravel())
        self.program["color"].value = tuple(color.ravel())
        self.vao.render(mode=mode)


class Triangle(RenderObj):
    def get_verts(self):
        return np.array([
            -0.5, -0.5, 0.0,
            0.0, 0.5, 0.0,
            0.5, -0.5, 0.0
        ], dtype=np.float32)


class House(RenderObj):
    def get_verts(self):
        return 5 * np.array([
            -1, -1, -1,
            1, -1, -1,
            1, -1, 1,
            -1, -1, 1,
            -1, -1, -1,
            -1, 1, -1,
            1, 1, -1,
            1, 1, 1,
            -1, 1, 1,
            -1, 1, -1,

            1, 1, -1,
            1, -1, -1,
            1, 1, -1,

            1, 1, 1,
            1, -1, 1,
            1, 1, 1,

            -1, 1, 1,
            -1, -1, 1,

            -0.25, -1, 1,
            -0.25, 0.5, 1,
            0.25, 0.5, 1,
            0.25, -1, 1,
            1, -1, 1,
            1, 1, 1,
            0, 1.75, 1,
            -1, 1, 1,
            0, 1.75, 1,
            0, 1.75, -1,
            1, 1, -1,
            0, 1.75, -1,
            -1, 1, -1
        ], dtype=np.float32)


class Car(RenderObj):
    def get_verts(self):
        return np.array([
            # front side
            -3, 1, 2,
            3, 1, 2,
            3, 2, 2,
            2, 3, 2,
            -2, 3, 2,
            -3, 2, 2,
            -3, 1, 2,

            # back side
            -3, 1, -2,
            3, 1, -2,
            3, 2, -2,
            2, 3, -2,
            -2, 3, -2,
            -3, 2, -2,
            -3, 1, -2,

            # connectors
            3, 1, -2,
            3, 1, 2,
            3, 2, 2,
            3, 2, -2,
            2, 3, -2,
            2, 3, 2,
            -2, 3, 2,
            -2, 3, -2,
            -3, 2, -2,
            -3, 2, 2
        ], dtype=np.float32)


class Tire(RenderObj):
    def get_verts(self):
        return np.array([
            -1, .5, .5,
            -.5, 1, .5,
            -.5, 1, .5,
            .5, 1, .5,
            .5, 1, .5,
            1, .5, .5,
            1, .5, .5,
            1, -.5, .5,
            1, -.5, .5,
            .5, -1, .5,
            .5, -1, .5,
            -.5, -1, .5,
            -.5, -1, .5,
            -1, -.5, .5,
            -1, -.5, .5,
            -1, .5, .5,
            #Back Side
            -1, .5, -.5,
            -.5, 1, -.5,
            -.5, 1, -.5,
            .5, 1, -.5,
            .5, 1, -.5,
            1, .5, -.5,
            1, .5, -.5,
            1, -.5, -.5,
            1, -.5, -.5,
            .5, -1, -.5,
            .5, -1, -.5,
            -.5, -1, -.5,
            -.5, -1, -.5,
            -1, -.5, -.5,
            -1, -.5, -.5,
            -1, .5, -.5,
            #Connectors
            -1, .5, .5,
            -1, .5, -.5,
            -.5, 1, .5,
            -.5, 1, -.5,
            .5, 1, .5,
            .5, 1, -.5,
            1, .5, .5,
            1, .5, -.5,
            1, -.5, .5,
            1, -.5, -.5,
            .5, -1, .5,
            .5, -1, -.5,
            -.5, -1, .5,
            -.5, -1, -.5,
            -1, -.5, .5,
            -1, -.5, -.5
        ], np.float32)