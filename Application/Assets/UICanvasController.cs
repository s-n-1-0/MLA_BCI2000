using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class UICanvasController : MonoBehaviour
{
    public TaskManager task;
    public TextMeshProUGUI trialsNumText,maxTrialsNumText,stimTimeText;

    private void Update()
    {
        trialsNumText.text = task.state.trialNum.ToString();
    }
    public void clickNFBButton(bool isNFB) => task.StartTask(isNFB);
    public void SetStimTIme(float time) => stimTimeText.text = $"Stim : {time}s";
    public void SetMaxTrialsNum(int num) =>maxTrialsNumText.text = $"Max : {num}" ;
    
}
