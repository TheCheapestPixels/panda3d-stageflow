#version 100

precision mediump float;
uniform sampler2D p3d_Texture0;
varying vec2 v_texcoord;
uniform float fade;
uniform float time;

void main () {
  // float v = pow(v_texcoord.x - 0.5, 2.0) + pow(v_texcoord.y - 0.5, 2.0);
  // v = mod(v * 10.0, 1.0);
  // float v = mod(time * 20.0, 1.0);
  //// UV-based flickering
  float v = mod(min(abs(v_texcoord.x - 0.5), abs(v_texcoord.y - 0.5)) * 20.0 - time * 10.0, 1.0);
  //// Screen coord based color background
  //vec2 screen_coord = gl_FragCoord.xy / viewPortSize;
  //float v = (screen_coord.x + screen_coord.y) / 2.0;

  float r = 0.0;
  float g = 0.0;
  float b = 0.0;

  if (v < 1.0/3.0) {
    float i = v * 3.0;
    r = 1.0 - i;
    g = i;
  }
  if (all(bvec2(1.0/3.0 <= v, v < 2.0/3.0))) {
    float i = (v - 1.0/3.0) * 3.0;
    g = 1.0 - i;
    b = i;
  }
  if (2.0/3.0 <= v) {
    float i = (v - 2.0/3.0) * 3.0;
    b = 1.0 - i;
    r = i;
  }

  r = sqrt(r);
  g = sqrt(g);
  b = sqrt(b);

  gl_FragColor = vec4(
    r * (1.0 - fade),
    g * (1.0 - fade),
    b * (1.0 - fade),
    0
  );
}
