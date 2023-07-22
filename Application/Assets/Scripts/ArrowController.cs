using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

public class ArrowController : MonoBehaviour
{
    public bool isArrowLeft = true;
    public bool isStripeSameDirectionAsArrow = true;
    public bool isStopedShift = false;
    public float shiftSpeed = 1f;
    [SerializeField]
    private ArrowType arrowType = ArrowType.Stripe; //typeの変更と同時にマテリアルも変更する必要があるためSetArrowTypeを使用
    public Material  defaultMat, stripeMat;
    private MeshRenderer mesh;
    private float shiftTime;
    void Awake()
    {
        mesh = gameObject.GetComponentInChildren<MeshRenderer>();
    }

    // Update is called once per frame
    public void Update()
    {
        if (!isStopedShift)
        {
            shiftTime += Time.deltaTime * (isStripeSameDirectionAsArrow ? -1 : 1);
            if (shiftTime > 1) shiftTime = shiftTime - 1;
            if (shiftTime < 0) shiftTime = 1 - shiftTime;
        }
        //mesh.material.SetFloat("_Speed", Mathf.Abs(shiftSpeed) * (isStripeSameDirectionAsArrow ? 1 : -1));
        mesh.material.SetFloat("_ShiftDistance", shiftTime * Mathf.Abs(shiftSpeed));
        SetEulerAngles();
    }
    private void OnValidate()
    {
        SetArrowType(arrowType);
    }
    public void SetEulerAngles()
    {
        transform.eulerAngles = new Vector3(90, (isArrowLeft ? 0f : 180f), 0f);
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

