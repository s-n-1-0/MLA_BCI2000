﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowController : MonoBehaviour
{
    public bool isArrowLeft = true;
    public bool isStripeSameDirectionAsArrow = true;
    public float shiftSpeed = 0.1f;
    private MeshRenderer mesh;
    void Start()
    {
        mesh = GetComponent<MeshRenderer>();
    }

    // Update is called once per frame
    void Update()
    {
        mesh.material.SetFloat("_Speed", Mathf.Abs(shiftSpeed) * (isStripeSameDirectionAsArrow ? 1:-1));
        transform.eulerAngles = new Vector3(90f + (isArrowLeft ? 0f : 180f),90f,90f);
    }
}
