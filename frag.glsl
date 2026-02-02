#version 450

out vec4 fragment_color;

uniform sampler2DArray texture_array_sampler;

in vec3 local_position;
in vec3 interpolated_tex_coords;

void main(void) {
    //fragment_color = vec4(local_position / 2.0 + 0.5, 1.0);
    // Z coordinate is the index of the texture in the texture array.
    // The following code samples the center of the first loaded texture.
    //fragment_color = texture(texture_array_sampler, vec3(0.5, 0.5, 0.0));

    // To sample the texture at different places depending on where the fragment is on the block face,
    // we use a different texture coordinate for each vertex and interpolate between them for each fragment.
    // For example, from left to right we might go from left:0 to right:1 by increments.
    fragment_color = texture(texture_array_sampler, interpolated_tex_coords);


}