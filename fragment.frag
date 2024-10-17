#version 330 core
out vec4 FragColor;

uniform vec2 resolution;
uniform float time;
uniform float zoom;
uniform vec3 colorMode;
uniform vec2 move;

vec3 z_solver(vec2 c, int max_iterations) {
    vec2 z = vec2(0.0, 0.0);
    for (int k = 0; k < max_iterations; k++) {
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
        float d = sqrt(pow(z.x,2) + pow(z.y,2));
        if (d > 2.0) {
            float x = float(k) / float(max_iterations);
            return vec3(x) * colorMode;
        }
    }
    return vec3(0.0, 0.0, 0.0);
}

void main() {
    vec2 uv = (gl_FragCoord.xy - 0.5 * resolution.xy) / resolution.y;
    uv += move;
    vec2 c = uv * (4.0 / zoom);
    vec3 color = z_solver(c, 500);
    FragColor = vec4(color, 1.0);
}