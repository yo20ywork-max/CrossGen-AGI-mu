import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: win
    visible: true; width: 780; height: 640; minimumWidth: 700; minimumHeight: 590
    title: "CrossGen-AGI-μ｜安裝與控制台"
    font.family: "Microsoft JhengHei UI"; font.pixelSize: 14
    onClosing: function(event) { event.accepted=setup.canExit;if (!setup.canExit) setup.closeAll() }
    background: Rectangle { gradient: Gradient { orientation: Gradient.Horizontal
        GradientStop { position: 0; color: "#edf8ff" }
        GradientStop { position: 0.5; color: "#f5efff" }
        GradientStop { position: 1; color: "#fff2ec" }
    } }
    component Action: Button {
        id: button; implicitHeight: 44; horizontalPadding: 20
        property bool primary: false
        background: Rectangle { radius: 10; color: button.primary ? "#e0d7f8" : button.hovered ? "#edf0fa" : "#ffffff"; border.color: "#d6ddee"; opacity: button.enabled ? 1 : 0.5 }
        contentItem: Text { text: button.text; color: button.enabled ? "#172445" : "#7b8398"; font: button.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
    }
    ColumnLayout {
        anchors.fill: parent; anchors.margins: 34; spacing: 18
        RowLayout { spacing: 16
            Rectangle { width: 70; height: 56; radius: 12; color: "white"; border.color: "#dce1f0"
                Image { anchors.fill: parent; anchors.margins: 7; source: "company-mark.png"; fillMode: Image.PreserveAspectFit; mipmap: true }
            }
            Column { spacing: 4
                Text { text: "CrossGen-AGI-μ"; color: "#172445"; font.pixelSize: 25; font.weight: Font.DemiBold }
                Text { text: "跨世代媒體科技股份有限公司 · TAIWAN"; color: "#5e6b85"; font.pixelSize: 12 }
            }
        }
        Text { text: setup.ready ? "準備好，開始工作。" : "一次設定，就能開始。"; color: "#172445"; font.pixelSize: 28; font.weight: Font.DemiBold }
        Text { text: "自動安裝程式、主模型、語音辨識與瀏覽器元件。\nWindows 11 · 建議24GB記憶體 · 安裝磁碟預留25GB"; color: "#5e6b85"; lineHeight: 1.5; font.pixelSize: 13 }
        Rectangle { Layout.fillWidth: true; Layout.fillHeight: true; radius: 16; color: "#ffffff"; border.color: "#dce1f0"
            ColumnLayout { anchors.fill: parent; anchors.margins: 24; spacing: 14
                Text { text: setup.status; color: "#172445"; font.pixelSize: 18; font.weight: Font.DemiBold; wrapMode: Text.Wrap; Layout.fillWidth: true }
                ProgressBar { Layout.fillWidth: true; from: 0; to: 1; value: setup.progress; indeterminate: setup.busy && setup.progress===0 && !setup.authCode }
                Text { text: setup.detail; color: "#5e6b85"; font.pixelSize: 13; wrapMode: Text.Wrap; Layout.fillWidth: true; textFormat: Text.PlainText }
                RowLayout { visible: !!setup.authCode
                    Text { text: "授權碼："+setup.authCode; color: "#6050b5"; font.pixelSize: 20; font.bold: true }
                    Action { text: "開啟登入頁"; onClicked: setup.openAuth() }
                }
                Item { Layout.fillHeight: true }
                Text { text: "安裝位置："+setup.installPath; color: "#788198"; font.pixelSize: 11; wrapMode: Text.WrapAnywhere; Layout.fillWidth: true }
            }
        }
        RowLayout { Layout.fillWidth: true; spacing: 10
            Action { text: setup.ready ? "檢查／修復安裝" : "開始自動安裝"; primary: true; enabled: !setup.busy; onClicked: setup.install() }
            Action { text: "開啟 CrossGen"; enabled: setup.ready && !setup.busy; onClicked: setup.launch() }
            Item { Layout.fillWidth: true }
            Action { objectName: "closeAllButton"; text: "一鍵全部關閉"; onClicked: setup.closeAll() }
        }
        RowLayout { Layout.fillWidth: true
            Action { text: "麥克風權限設定"; implicitHeight: 32; font.pixelSize: 11; onClicked: setup.microphoneSettings() }
            Text { text: "關閉控制台也會停止它啟動的程式與模型服務。"; color: "#5e6b85"; font.pixelSize: 11; Layout.fillWidth: true; wrapMode: Text.Wrap }
        }
    }
}
