using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowController : MonoBehaviour
{
    //public bool isLeft = true;
    public float shiftSpeed = 0.1f;
    private MeshRenderer mesh;
    void Start()
    {
        mesh = GetComponent<MeshRenderer>();
    }

    // Update is called once per frame
    void Update()
    {
        mesh.material.SetFloat("_Speed", shiftSpeed);   
    }
}
