#version 450

layout(location = 0) in vec3 vertex_position; // vertex position attribute
layout(location = 1) in vec3 tex_coords; // texture coordinates attribute
layout(location = 2) in float shading_values; // shading values attribute

out vec3 local_position;
out vec3 interpolated_tex_coords;
out float interpolated_shading_values;

uniform mat4 matrix;

void main(void) {
    local_position = vertex_position;
    interpolated_tex_coords = tex_coords;
    interpolated_shading_values = shading_values;
    gl_Position = matrix * vec4(vertex_position, 1.0);
}