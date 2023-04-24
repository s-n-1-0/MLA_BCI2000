using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BCIManager : CustomVariableBase
{
    public int yClass;
    public ArrowController arrowController;
    public override void AddCustomVariables()
    {
        //TODO: 適切な変数指定
        customVariables.Add(new CustomGetVariable(
            "YClass",
            new Action<int>((int i) => { yClass = i; })
        ));
    }
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        //TODO: クラス分類結果に応じた矢印設定
        switch (yClass)
        {
            case 0:
                break;
        }
    }
}
