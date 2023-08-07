using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class UICanvasController : MonoBehaviour
{
    public TaskManager task;
    public TextMeshProUGUI trialsNumText,maxTrialsNumText,stimTimeText;
    public GameObject announcePanel;
    private void Update()
    {
        trialsNumText.text = task.state.trialNum.ToString();
    }
    public void ToggleAnnouncePanel() => announcePanel.SetActive(!announcePanel.activeSelf);
    public void ClickNFBButton(bool isNFB) => task.StartTask(isNFB);
    public void SetStimTIme(float time) => stimTimeText.text = $"Stim : {time}s";
    public void SetMaxTrialsNum(int num) =>maxTrialsNumText.text = $"Max : {num}" ;
    
}
