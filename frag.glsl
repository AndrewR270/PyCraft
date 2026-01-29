#version 450

out vec4 fragment_color;

in vec3 local_position;

void main(void) {
    fragment_color = vec4(local_position / 2.0 + 0.5, 1.0);
}