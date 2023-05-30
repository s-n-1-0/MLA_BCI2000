using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class UICanvasController : MonoBehaviour
{
    public TaskManager task;
    public TextMeshProUGUI text;
    private void Update()
    {
        text.text = task.state.trialNum.ToString();
    }
    public void clickNFBButton(bool isNFB) => task.StartTask(isNFB);
}
