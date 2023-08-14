using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class UICanvasController : MonoBehaviour
{
    public TaskManager task;
    public TextMeshProUGUI trialsNumText, maxTrialsNumText, stimTimeText;
    public GameObject announcePanel, testPanel, trainPanel;
    private void Update()
    {
        trialsNumText.text = task.state?.trialNum.ToString() ?? "";
    }
    public void ToggleAnnouncePanel() => announcePanel.SetActive(!announcePanel.activeSelf);
    public void ToggleTestPanel() => testPanel.SetActive(!testPanel.activeSelf);
    public void ToggleTrainPanel() => trainPanel.SetActive(!trainPanel.activeSelf);
    public void ClickNFBButton(bool isNFB)
    {
        testPanel.SetActive(false);
        trainPanel.SetActive(false);
        task.StartTask(isNFB);
    }
    public void SetStimTIme(float time) => stimTimeText.text = $"Stim : {time}s";
    public void SetMaxTrialsNum(int num) =>maxTrialsNumText.text = $"Max : {num}" ;
    
}
