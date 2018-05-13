//
// Copyright 2016 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
import UIKit
import AVFoundation
import googleapis
import SpeechKit
import Firebase

let SAMPLE_RATE = 16000

class ViewController : UIViewController, AudioControllerDelegate, SKTransactionDelegate {
  @IBOutlet weak var textView: UITextView!
    
    private let audioEngine = AVAudioEngine()
  var audioData: NSMutableData!

  override func viewDidLoad() {
    super.viewDidLoad()
    AudioController.sharedInstance.delegate = self
  }

    @IBAction func tappedButton(sender: AnyObject) {
        startlistening()
    }
    func startlistening(){
        try! startRecording()
        // All fields are required.
        // Your credentials can be found in your Nuance Developers portal, under "Manage My Apps".
        let SKSAppKey = "e36d3e3f195339085942653c40122ce899dc91a60894900d69c6fd417296785504b6951d09ce2563108a9f509dcc3836a8c9dcb05e6cbdc732bb08a55181fa55";
        let SKSAppId = "NMDPPRODUCTION_dialog_system_dialog_system_20180320214426";
        let SKSServerHost = "lsr.nmdp.nuancemobility.net";
        let SKSServerPort = "443";
        
        let SKSLanguage = "jpn-JPN";
        
        let SKSServerUrl = "nmsps://\(SKSAppId)@\(SKSServerHost):\(SKSServerPort)"
        
        let session = SKSession(url: NSURL(string: SKSServerUrl)! as URL, appToken: SKSAppKey)
        
        
        //this starts a transaction that listens for voice input
        let transaction = session?.recognize(withType:SKTransactionSpeechTypeDictation,
                                             detection: .short,
                                             language: SKSLanguage,
                                             delegate: self)
    }
    private func startRecording() throws {
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(AVAudioSessionCategoryRecord)
        } catch {
            
        }
        audioData = NSMutableData()
        _ = AudioController.sharedInstance.prepare(specifiedSampleRate: SAMPLE_RATE)
        SpeechRecognitionService.sharedInstance.sampleRate = SAMPLE_RATE
        _ = AudioController.sharedInstance.start()
        textView.text = "Pepper:I'm listening"
    }
    func transactionDidBeginRecording(_ transaction: SKTransaction!) {
        print("doing")
    }
    func transactionDidFinishRecording(_ transaction: SKTransaction!) {
        print("ending")
        audioEngine.stop()
        _ = AudioController.sharedInstance.stop()
        SpeechRecognitionService.sharedInstance.stopStreaming()
        //recordButton.isEnabled = false
        let dispatchTime: DispatchTime = DispatchTime.now() + Double(Int64(1.0 * Double(NSEC_PER_SEC))) / Double(NSEC_PER_SEC)
        DispatchQueue.main.asyncAfter(deadline: dispatchTime, execute: {
            self.startlistening()
        })
    }
    func transaction(_ transaction: SKTransaction!, didReceive recognition: SKRecognition!) {
        
        
    }
    private func transaction(transaction: SKTransaction!, didReceiveServiceResponse response: [NSObject : AnyObject]!) {  }
    func transaction(transaction: SKTransaction!, didFinishWithSuggestion suggestion: String!) {  }
    func transaction(transaction: SKTransaction!, didFailWithError error: NSError!, suggestion: String!) {  }
    
  func processSampleData(_ data: Data) -> Void {
    audioData.append(data)

    // We recommend sending samples in 100ms chunks
    let chunkSize : Int /* bytes/chunk */ = Int(0.1 /* seconds/chunk */
      * Double(SAMPLE_RATE) /* samples/second */
      * 2 /* bytes/sample */);

    if (audioData.length > chunkSize) {
      SpeechRecognitionService.sharedInstance.streamAudioData(audioData,
                                                              completion:
        { [weak self] (response, error) in
            guard let strongSelf = self else {
                return
            }
            
            if let error = error {
                print(error.localizedDescription)
            } else if let response = response {
                var finished = false
                for result in response.resultsArray! {
                    if let result = result as? StreamingRecognitionResult {
                        if result.isFinal {
                            finished = true
                        }
                    }
                }
                if finished {
                    let tmpBestResult = (response.resultsArray.firstObject as! StreamingRecognitionResult)
                    let tmpBestAlternativeOfResult = tmpBestResult.alternativesArray.firstObject as! SpeechRecognitionAlternative
                    let bestTranscript = tmpBestAlternativeOfResult.transcript
                    print(bestTranscript!)
                    self?.textView.text = bestTranscript!
                    var ref = Database.database().reference()
                    ref.child("message-top").setValue(bestTranscript!)
                }
            }
      })
      self.audioData = NSMutableData()
    }
  }
}
