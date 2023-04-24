using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

public class ArrowController : MonoBehaviour
{
    public bool isArrowLeft = true;
    public bool isStripeSameDirectionAsArrow = true;
    public float shiftSpeed = 0.1f;
    public ArrowType arrowType = ArrowType.Stripe;
    public Material  defaultMat, stripeMat;
    private MeshRenderer mesh;
    void Start()
    {
        mesh = GetComponent<MeshRenderer>();
    }

    // Update is called once per frame
    void Update()
    {
         mesh.material.SetFloat("_Speed", Mathf.Abs(shiftSpeed) * (isStripeSameDirectionAsArrow ? 1 : -1));
        transform.eulerAngles = new Vector3(90f + (isArrowLeft ? 0f : 180f), 90f, 90f);
    }
    private void OnValidate()
    {
        if (mesh)  mesh.material = arrowType == ArrowType.Default ? defaultMat : stripeMat;
    }
}
public enum ArrowType {
    Default,
    Stripe
}

