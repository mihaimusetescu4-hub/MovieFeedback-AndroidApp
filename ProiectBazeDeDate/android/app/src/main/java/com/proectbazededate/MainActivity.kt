package com.proiectbazededate

import android.os.Bundle
import com.facebook.react.ReactActivity
import com.facebook.react.ReactActivityDelegate
import com.facebook.react.defaults.DefaultNewArchitectureEntryPoint
import com.facebook.react.defaults.DefaultReactActivityDelegate

class MainActivity : ReactActivity() {

  override fun getMainComponentName(): String = "ProiectBazeDeDate"

  override fun createReactActivityDelegate(): ReactActivityDelegate {
    return DefaultReactActivityDelegate(
      this,
      mainComponentName,
      // AICI ESTE CORECȚIA:
      // În loc de .getFabricEnabled(), folosim .fabricEnabled
      DefaultNewArchitectureEntryPoint.fabricEnabled
    )
  }

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(null)
  }
}