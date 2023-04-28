using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
/**
 * MLASceneを追加読み込みする(1回限り)
 */
public class MLASceneLoader : MonoBehaviour
{
    public GameObject bci2000;
    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(_Start());
    }
    IEnumerator _Start()
    {
        var ld = SceneManager.LoadSceneAsync("MLAScene", LoadSceneMode.Additive);
        yield return ld;
        bci2000?.SetActive(true);
    }
}
