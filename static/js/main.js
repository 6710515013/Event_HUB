// =====================================================================
// EventHub - JavaScript ส่วนกลาง
// ใส่เฉพาะโค้ดที่ทุกหน้าใช้ร่วมกัน ถ้าใช้หน้าเดียวให้ใส่ใน {% block extra_js %} ของหน้านั้น
// =====================================================================

document.addEventListener("DOMContentLoaded", function () {
    hideSuccessAlerts();
    shadowNavbarOnScroll();
    preventDoubleSubmit();
    setupPasswordFields();
    setupCopyButtons();

    // แถบที่นั่งและนับถอยหลัง: อัปเดตทุก 30 วินาที
    // (Student Dashboard โหลดผลค้นหาใหม่โดยไม่รีเฟรชหน้า จึงต้องเช็คซ้ำเรื่อยๆ)
    updateSeatBars();
    updateCountdowns();
    setInterval(function () {
        updateSeatBars();
        updateCountdowns();
    }, 30000);

    // เมื่อหน้า Dashboard เปลี่ยนรายการกิจกรรม ให้วาดแถบที่นั่งและนับถอยหลังทันที
    var observer = new MutationObserver(function () {
        updateSeatBars();
        updateCountdowns();
    });
    observer.observe(document.body, { childList: true, subtree: true });
});


// ---------------------------------------------------------------------
// 1. กล่องแจ้งเตือนสำเร็จ (สีเขียว) ปิดเองหลัง 5 วินาที
//    กล่อง error ไม่ปิดเอง เพื่อให้ผู้ใช้อ่านได้ครบ
// ---------------------------------------------------------------------
function hideSuccessAlerts() {
    document.querySelectorAll(".alert-success.alert-dismissible").forEach(function (alertBox) {
        setTimeout(function () {
            bootstrap.Alert.getOrCreateInstance(alertBox).close();
        }, 5000);
    });
}


// ---------------------------------------------------------------------
// 2. Navbar มีเงาเมื่อเลื่อนหน้าลง
// ---------------------------------------------------------------------
function shadowNavbarOnScroll() {
    var navbar = document.querySelector(".eh-navbar");
    if (!navbar) {
        return;
    }
    function update() {
        navbar.classList.toggle("eh-scrolled", window.scrollY > 4);
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
}


// ---------------------------------------------------------------------
// 3. กันกดปุ่มซ้ำ: ฟอร์ม POST ทุกฟอร์ม เมื่อกดส่งแล้วปุ่มจะกดไม่ได้
//    และขึ้นข้อความ "กำลังดำเนินการ..." พร้อมไอคอนหมุน
//    เปลี่ยนข้อความได้ด้วย data-loading-text="กำลังสมัคร..." ที่ปุ่ม
// ---------------------------------------------------------------------
function preventDoubleSubmit() {
    document.querySelectorAll('form[method="post"], form[method="POST"]').forEach(function (form) {
        form.addEventListener("submit", function (event) {
            var button = event.submitter || form.querySelector('button[type="submit"]');
            if (!button || button.classList.contains("is-loading")) {
                return;
            }
            var text = button.dataset.loadingText || "กำลังดำเนินการ...";

            // ปิดปุ่มหลังเบราว์เซอร์ส่งฟอร์มไปแล้ว ไม่อย่างนั้นค่าของปุ่มจะไม่ถูกส่ง
            setTimeout(function () {
                if (event.defaultPrevented) {
                    return;
                }
                button.dataset.originalHtml = button.innerHTML;
                button.classList.add("is-loading");
                button.setAttribute("aria-disabled", "true");
                button.disabled = true;
                button.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>' + text;
            }, 0);
        });
    });

    // กดปุ่มย้อนกลับของเบราว์เซอร์แล้วกลับมาหน้านี้ ให้ปุ่มกดได้อีกครั้ง
    window.addEventListener("pageshow", function (event) {
        if (!event.persisted) {
            return;
        }
        document.querySelectorAll(".btn.is-loading").forEach(function (button) {
            button.classList.remove("is-loading");
            button.removeAttribute("aria-disabled");
            button.disabled = false;
            if (button.dataset.originalHtml) {
                button.innerHTML = button.dataset.originalHtml;
            }
        });
    });
}


// ---------------------------------------------------------------------
// 4. ช่องรหัสผ่าน: ปุ่มรูปตา (.eh-eye) และเตือน Caps Lock (.eh-caps)
//    HTML ที่ต้องมี:
//    <div class="eh-password">
//      <input type="password" id="id_password">
//      <button type="button" class="eh-eye" data-target="id_password">...</button>
//    </div>
//    <small class="eh-caps" hidden>Caps Lock เปิดอยู่</small>
// ---------------------------------------------------------------------
function setupPasswordFields() {
    document.querySelectorAll(".eh-eye").forEach(function (button) {
        button.addEventListener("click", function () {
            var input = document.getElementById(button.dataset.target);
            if (!input) {
                return;
            }
            var isHidden = input.type === "password";
            input.type = isHidden ? "text" : "password";
            button.setAttribute("aria-label", isHidden ? "ซ่อนรหัสผ่าน" : "แสดงรหัสผ่าน");
            button.querySelector("i").className = isHidden ? "bi bi-eye-slash" : "bi bi-eye";
        });
    });

    document.querySelectorAll(".eh-password input").forEach(function (input) {
        var hint = input.closest(".eh-field") && input.closest(".eh-field").querySelector(".eh-caps");
        if (!hint) {
            return;
        }
        function check(event) {
            if (event.getModifierState) {
                hint.hidden = !event.getModifierState("CapsLock");
            }
        }
        input.addEventListener("keydown", check);
        input.addEventListener("keyup", check);
        input.addEventListener("blur", function () {
            hint.hidden = true;
        });
    });
}


// ---------------------------------------------------------------------
// 5. ปุ่มคัดลอกข้อความ: <button data-eh-copy="ข้อความ">คัดลอก</button>
// ---------------------------------------------------------------------
function setupCopyButtons() {
    document.querySelectorAll("[data-eh-copy]").forEach(function (button) {
        button.addEventListener("click", function () {
            var original = button.innerHTML;
            navigator.clipboard.writeText(button.dataset.ehCopy).then(function () {
                button.innerHTML = '<i class="bi bi-check2"></i> คัดลอกแล้ว';
                setTimeout(function () {
                    button.innerHTML = original;
                }, 1800);
            }).catch(function () {
                window.prompt("คัดลอกลิงก์นี้", button.dataset.ehCopy);
            });
        });
    });
}


// ---------------------------------------------------------------------
// 6. จำนวนผู้สนใจ: <div class="eh-seat" data-count="28" data-max="40"></div>
//    ไม่จำกัดจำนวนคนกดสมัคร (ผู้จัดคัดเลือกผ่าน Google Form)
//    จึงแสดงแค่ "สนใจแล้ว N คน" และ "รับ M คน" ไม่มีคำว่าเต็ม
// ---------------------------------------------------------------------
function updateSeatBars() {
    document.querySelectorAll(".eh-seat:not([data-ready])").forEach(function (seat) {
        var count = parseInt(seat.dataset.count, 10) || 0;
        var max = parseInt(seat.dataset.max, 10) || 0;

        seat.innerHTML =
            '<div class="eh-seat-label">' +
                '<span><i class="bi bi-people"></i> สนใจแล้ว ' + count + " คน</span>" +
                (max > 0 ? "<span>รับ " + max + " คน</span>" : "") +
            "</div>";
        seat.dataset.ready = "true";
    });
}


// ---------------------------------------------------------------------
// 7. นับถอยหลังปิดรับสมัคร: <span class="eh-countdown" data-deadline="2026-11-20T23:59:00+07:00"></span>
//    เหลือน้อยกว่า 24 ชม. = สีส้ม, เลยกำหนด = "ปิดรับสมัครแล้ว"
// ---------------------------------------------------------------------
function updateCountdowns() {
    var now = Date.now();
    document.querySelectorAll(".eh-countdown[data-deadline]").forEach(function (box) {
        var deadline = new Date(box.dataset.deadline).getTime();
        if (isNaN(deadline)) {
            return;
        }
        var diff = deadline - now;
        var text;

        box.classList.remove("is-urgent", "is-ended");
        if (diff <= 0) {
            box.classList.add("is-ended");
            text = "ปิดรับสมัครแล้ว";
        } else {
            var minutes = Math.floor(diff / 60000);
            var days = Math.floor(minutes / 1440);
            var hours = Math.floor((minutes % 1440) / 60);
            var mins = minutes % 60;

            if (days > 0) {
                text = "ปิดรับในอีก " + days + " วัน " + hours + " ชม.";
            } else if (hours > 0) {
                text = "ปิดรับในอีก " + hours + " ชม. " + mins + " นาที";
            } else {
                text = "ปิดรับในอีก " + Math.max(mins, 1) + " นาที";
            }
            if (diff < 24 * 60 * 60 * 1000) {
                box.classList.add("is-urgent");
            }
        }

        var newHtml = '<i class="bi bi-clock"></i><span>' + text + "</span>";
        if (box.innerHTML !== newHtml) {
            box.innerHTML = newHtml;
        }
    });
}
