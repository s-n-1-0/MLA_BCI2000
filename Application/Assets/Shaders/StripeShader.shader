Shader "Custom/TimeStripeShader2" {
    Properties{
        _MainTex("Texture", 2D) = "white" {}
        _StripeWidth("Stripe Width", Range(0, 1)) = 0.05
        _Speed("Speed", Range(-10, 10)) = 1
        _Direction("Shift Direction", Range(0, 1)) = 0
    }
        SubShader{
            Tags {"Queue" = "Transparent" "RenderType" = "Opaque"}
            LOD 100
            Cull Off
            Pass {
                CGPROGRAM
                #pragma vertex vert
                #pragma fragment frag
                #include "UnityCG.cginc"

                struct appdata {
                    float4 vertex : POSITION;
                    float2 uv : TEXCOORD0;
                };

                struct v2f {
                    float2 uv : TEXCOORD0;
                    float4 vertex : SV_POSITION;
                };

                sampler2D _MainTex;
                float _StripeWidth;
                float _Speed;
                float _Direction;

                v2f vert(appdata v) {
                    v2f o;
                    o.vertex = UnityObjectToClipPos(v.vertex);
                    o.uv = v.uv;
                    return o;
                }

                fixed4 frag(v2f i) : SV_Target {
                    float time = _Time.y * _Speed;
                    float shift = fmod(time, _StripeWidth);
                    if (_Direction > 0.5) {
                        shift = _StripeWidth - shift;
                    }
                    float u = fmod((i.uv.x + shift) / _StripeWidth, 1.0);
                    if (u < 0.5) {
                        return tex2D(_MainTex, i.uv);
                    }
     else {
      return float4(0, 0, 0, 1);
  }
}
ENDCG
}
        }
            FallBack "Diffuse"
}