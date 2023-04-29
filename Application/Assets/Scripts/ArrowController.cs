using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

public class ArrowController : MonoBehaviour
{
    public bool isArrowLeft = true;
    public bool isStripeSameDirectionAsArrow = true;
    public float shiftSpeed = 0.1f;
    [SerializeField]
    private ArrowType arrowType = ArrowType.Stripe; //typeの変更と同時にマテリアルも変更する必要があるためSetArrowTypeを使用
    public Material  defaultMat, stripeMat;
    private MeshRenderer mesh;
    void Awake()
    {
        mesh = gameObject.GetComponentInChildren<MeshRenderer>();
    }

    // Update is called once per frame
    public void Update()
    {
         mesh.material.SetFloat("_Speed", Mathf.Abs(shiftSpeed) * (isStripeSameDirectionAsArrow ? 1 : -1));
        transform.eulerAngles = new Vector3(90f + (isArrowLeft ? 0f : 180f), 90f, 90f);
    }
    private void OnValidate()
    {
        SetArrowType(arrowType);
    }
    public void SetArrowType(ArrowType type)
    {
        arrowType = type;
        if (mesh) mesh.material = arrowType == ArrowType.Default ? defaultMat : stripeMat;
    }
}
public enum ArrowType {
    Default,
    Stripe
}

