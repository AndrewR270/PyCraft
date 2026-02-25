#version 450

out vec4 fragment_color;

uniform sampler2DArray texture_array_sampler;

in vec3 local_position;
in vec3 interpolated_tex_coords;
in float interpolated_shading_values;

void main(void) {
    vec4 texture_color = texture(texture_array_sampler, interpolated_tex_coords);
    fragment_color = texture_color * interpolated_shading_values;

    if (texture_color.a == 0.0) { discard; }
}