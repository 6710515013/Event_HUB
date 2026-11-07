document.addEventListener("DOMContentLoaded", function () {

    // ซ่อนกล่องแจ้งเตือนสำเร็จ (สีเขียว) อัตโนมัติหลัง 5 วินาที
    // กล่องแจ้งเตือน error ไม่ซ่อนเอง เพื่อให้ผู้ใช้อ่านได้ครบ
    document.querySelectorAll(".alert-success.alert-dismissible").forEach(function (alertBox) {
        setTimeout(function () {
            bootstrap.Alert.getOrCreateInstance(alertBox).close();
        }, 5000);
    });

});