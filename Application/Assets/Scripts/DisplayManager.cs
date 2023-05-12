using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DisplayManager : MonoBehaviour
{
    [SerializeField, Range(1, 8)]
    private int displayCount = 2;

    private void Awake()
    {
        int count = Mathf.Min(Display.displays.Length, displayCount);

        for (int i = 0; i < count; ++i)
        {
            Display.displays[i].Activate();
        }
    }
}
