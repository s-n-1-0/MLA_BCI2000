using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BVREventController : MonoBehaviour
{
    public bool isEvent = false;
    public Image marker;
    // Update is called once per frame
    void Update()
    {
        if (isEvent)
        {
            isEvent = false;
            marker.enabled = true;
        }
        else
        {
            marker.enabled = false;
        }
    }
}
