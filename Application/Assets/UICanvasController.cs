using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UICanvasController : MonoBehaviour
{
    public TaskManager task;
    public void clickNFBButton(bool isNFB) => task.StartTask(isNFB);
}
