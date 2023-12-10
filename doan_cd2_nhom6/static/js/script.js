document.addEventListener("DOMContentLoaded", function () {
    // Lấy tất cả các nút "Reply" và biểu mẫu reply
    var replyButtons = document.querySelectorAll(".replyButton");
    var replyForms = document.querySelectorAll(".replyForm");

    // Lặp qua từng nút "Reply"
    replyButtons.forEach(function (button, index) {
        // Gán sự kiện khi nút "Reply" được nhấp
        button.addEventListener("click", function () {
            // Ẩn tất cả các biểu mẫu reply
            replyForms.forEach(function (form) {
                form.style.display = "none";
            });

            // Hiển thị hoặc ẩn biểu mẫu reply tương ứng
            var currentForm = replyForms[index];
            currentForm.style.display = currentForm.style.display === "none" ? "block" : "none";
        });
    });
});
