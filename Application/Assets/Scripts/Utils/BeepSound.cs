using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[RequireComponent(typeof(AudioSource))]
public class BeepSound : MonoBehaviour
{
    public int startingPitch = 4;
    public int timeToDecrease = 5;
    AudioSource audioSource;
    private void Awake()
    {
        audioSource = GetComponent<AudioSource>();
    }

    public void Beep()
    {
        //Initialize the pitch
        audioSource.pitch = startingPitch;
        audioSource.Play();
    }

    void Update()
    {
        //While the pitch is over 0, decrease it as time passes.
        if (audioSource.pitch > 2)
        {
            audioSource.pitch += Time.deltaTime * startingPitch / timeToDecrease;
        }
    }
}
