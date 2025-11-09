const API_URL = "http://localhost:5001";

function showStatus(message, type) {
  const statusDiv = document.getElementById("status");
  statusDiv.textContent = message;
  statusDiv.className = `status ${type}`;
  statusDiv.style.display = "block";
}

function showProgress(show) {
  const progressDiv = document.getElementById("progress");
  progressDiv.style.display = show ? "block" : "none";
}

async function checkProgress(taskId) {
  try {
    const response = await fetch(`${API_URL}/progress/${taskId}`);
    const data = await response.json();

    if (data.status === "processing") {
      const progressText = `${data.message} (${data.completed}/${data.total})`;
      showStatus(progressText, "info");

      // 진행률 바 업데이트
      const progressBar = document.querySelector(".progress-bar");
      if (progressBar) {
        progressBar.style.width = `${data.progress}%`;
        progressBar.style.animation = "none";
      }

      // 계속 체크
      setTimeout(() => checkProgress(taskId), 2000);
    } else if (data.status === "completed") {
      showStatus(data.message + " - 다운로드를 시작합니다...", "success");

      // 파일 다운로드
      const downloadUrl = `${API_URL}${data.download_url}`;
      const a = document.createElement("a");
      a.href = downloadUrl;
      a.download = "";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      setTimeout(() => {
        showStatus("다운로드가 완료되었습니다! 🎉", "success");
        showProgress(false);
        document.getElementById("uploadBtn").disabled = false;
      }, 1000);
    } else if (data.status === "error") {
      showStatus(`오류: ${data.message}`, "error");
      showProgress(false);
      document.getElementById("uploadBtn").disabled = false;
    }
  } catch (error) {
    showStatus(`오류 발생: ${error.message}`, "error");
    showProgress(false);
    document.getElementById("uploadBtn").disabled = false;
  }
}

async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");

  if (!fileInput.files.length) {
    showStatus("파일을 선택해주세요", "error");
    return;
  }

  const file = fileInput.files[0];

  const validExtensions = [".xlsx", ".xls", ".csv", ".numbers"];
  const isValid = validExtensions.some((ext) =>
    file.name.toLowerCase().endsWith(ext)
  );

  if (!isValid) {
    showStatus(
      "엑셀(.xlsx, .xls), CSV(.csv), Numbers(.numbers) 파일만 업로드 가능합니다",
      "error"
    );
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  uploadBtn.disabled = true;
  showStatus("업로드 중... 잠시만 기다려주세요", "info");
  showProgress(true);

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      showStatus("파일 업로드 완료, 다운로드 시작...", "info");
      // 진행 상황 체크 시작
      checkProgress(data.task_id);
    } else {
      showStatus(`오류: ${data.error}`, "error");
      uploadBtn.disabled = false;
      showProgress(false);
    }
  } catch (error) {
    showStatus(`오류 발생: ${error.message}`, "error");
    uploadBtn.disabled = false;
    showProgress(false);
  }
}

// 파일 선택 시 상태 초기화
document.getElementById("fileInput").addEventListener("change", function () {
  const statusDiv = document.getElementById("status");
  statusDiv.style.display = "none";
});
