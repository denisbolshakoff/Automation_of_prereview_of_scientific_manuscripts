document.addEventListener("DOMContentLoaded", function() {

    const btn = document.getElementById("uploadBtn");
    const form = document.getElementById("uploadForm");
    const statusEl = document.querySelector(".status-message");
    const logo = document.querySelector("img.logo"); // логотип

    btn.addEventListener("click", async function() {
        
        btn.disabled = true;

      const fileInput = document.querySelector(".file-input");

        if (!fileInput.files.length) {
            alert("Выберите файл");
            return;
        }
       
        ["stage1","stage2","stage3"].forEach(id => {
    const el = document.getElementById(id);
    el.classList.remove("processing","done");
    el.querySelector(".stage-status").innerText = "…";
});


        document.getElementById("stage1").classList.add("processing");
        document.querySelector("#stage1 .stage-status").innerText = "⏳";

  

        const fileName = fileInput.files[0].name;

        ["second_message", "third_message", "fourth_message"].forEach(id => {
            const el = document.getElementById(id);
            el.textContent = "<обработка>";
            el.classList.add("empty-text");
            el.dataset.typed = "";
        });

        // Сообщение о начале обработки
        if (statusEl) statusEl.textContent = `Файл "${fileName}" обрабатывается…`;        
        document.body.style.cursor = "wait";

        // 🟢 Затемнение логотипа
        if (logo) logo.classList.add("loading");

        const formData = new FormData(form);

        try {
            let response = await fetch("/process", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                const errText = await response.text();
                alert("Ошибка сервера: " + errText);
                document.body.style.cursor = "default";
                if (logo) logo.classList.remove("loading"); // снять затемнение
                return;
            }

            let data = await response.json();
            const taskId = data.task_id;

            pollStatus(taskId, fileName, logo);

            form.reset();

        } catch (err) {
            console.error(err);
            alert("Произошла ошибка при отправке файла.");
            document.body.style.cursor = "default";
            if (logo) logo.classList.remove("loading"); // снять затемнение
        }

    });

});

async function pollStatus(taskId, fileName, logo) {

    const statusEl = document.querySelector(".status-message");

    const interval = setInterval(async () => {

        try {
            let response = await fetch("/status/" + taskId);

            if (!response.ok) {
                console.error("Ошибка запроса статуса:", response.status);
                clearInterval(interval);
                document.body.style.cursor = "default";
                if (logo) logo.classList.remove("loading");
                return;
            }

            let data = await response.json();

            const fields = [
                {id: "second_message", text: data.second_message},
                {id: "third_message", text: data.third_message},
                {id: "fourth_message", text: data.fourth_message}
            ];

            fields.forEach(f => {
                if (f.text) {
                    const el = document.getElementById(f.id);
                    if (el.textContent !== f.text) {
                        typeWriter(el, f.text, 10);
                    }
                    if (f.text !== "<обработка>") {
                        el.classList.remove("empty-text");
                    }
                }
            });

            if (data.status === "done") {
                clearInterval(interval);
                document.body.style.cursor = "default";

            const btn = document.getElementById("uploadBtn");
            btn.disabled = false;

            if (statusEl) statusEl.textContent = `Файл "${fileName}" обработан успешно.`;
                if (logo) logo.classList.remove("loading"); // снять затемнение
            }

            if (data.status === "error") {
                clearInterval(interval);
                alert("Ошибка обработки на сервере: " + data.error);
                document.body.style.cursor = "default";
                if (logo) logo.classList.remove("loading");
            }

            if (data.second_message) {

                document.getElementById("stage1").classList.remove("processing");
                document.getElementById("stage1").classList.add("done");
                document.querySelector("#stage1 .stage-status").innerText = "✓";

                document.getElementById("stage2").classList.add("processing");
                document.querySelector("#stage2 .stage-status").innerText = "⏳";
            }

            if (data.third_message) {

                document.getElementById("stage2").classList.remove("processing");
                document.getElementById("stage2").classList.add("done");
                document.querySelector("#stage2 .stage-status").innerText = "✓";

                document.getElementById("stage3").classList.add("processing");
                document.querySelector("#stage3 .stage-status").innerText = "⏳";
            }

            if (data.fourth_message) {

                document.getElementById("stage3").classList.remove("processing");
                document.getElementById("stage3").classList.add("done");
                document.querySelector("#stage3 .stage-status").innerText = "✓";
            }

        } catch (err) {
            console.error(err);
            clearInterval(interval);
            document.body.style.cursor = "default";
            if (logo) logo.classList.remove("loading");
        }

    }, 1000);

}

document.addEventListener("DOMContentLoaded", () => {
    const elementsToCheck = ["second_message", "third_message", "fourth_message"];

    elementsToCheck.forEach(id => {
        const el = document.getElementById(id);
       if (el && el.textContent.trim().includes("<пусто>")) {
            el.classList.add("empty-text");
        } else {
            el.classList.remove("empty-text"); // текст модели чёрный
        }
    });
});

function typeWriter(element, text, speed = 15) {
    if (element.dataset.typed) return;
    element.dataset.typed = "true";

    element.textContent = "";
    if (text !== "<обработка>") {
        element.classList.remove("empty-text"); // текст модели черный
    }

    let i = 0;
    function typing() {
        if (i < text.length) {
            element.textContent += text[i];
            i++;
            setTimeout(typing, speed);
        }
    }
    typing();
}