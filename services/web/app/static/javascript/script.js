document.addEventListener("DOMContentLoaded", function() {
    const visualizeButtons = document.querySelectorAll('.visualize-button');
    visualizeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const entryId = this.dataset.entryId; // 데이터 엔트리 ID를 가져옵니다.
            fetch(`/visualize/${entryId}`) // 시각화 데이터를 서버로부터 요청합니다.
                .then(response => response.json())
                .then(data => {
                    const modal = document.getElementById('myModal');
                    const summaryText = document.getElementById('summaryText');
                    const imageContainer = document.getElementById('modalImageContainer');

                    summaryText.innerHTML = `Domain 이름: ${entryId}`; // 요약 정보 업데이트
                    imageContainer.src = `data:image/png;base64,${data.plot_url}`; // 시각화 이미지 로드
                    modal.style.display = 'block'; // 모달 창 표시

                    event.stopPropagation(); // 이벤트 전파 중지
                })
                .catch(error => {
                    console.error('Error fetching the visualization:', error);
                });
        });
    });

    // 모달 외부 클릭 이벤트로 모달 닫기 설정
    window.onclick = function(event) {
        var modal = document.getElementById('myModal');
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    // 닫기 버튼 클릭 이벤트 설정
    var closeBtn = document.getElementsByClassName("close")[0];
    closeBtn.onclick = function() {
        document.getElementById('myModal').style.display = "none";
    };
});

// 토글 도메인 함수: 각 도메인의 URL을 숨기거나 표시
function toggleDomain(domainId, event) {
    var rows = document.getElementsByClassName(domainId);
    for (var i = 0; i < rows.length; i++) {
        rows[i].style.display = rows[i].style.display === 'none' ? '' : 'none';
    }
    event.stopPropagation();  // 클릭 이벤트 전파 중지
}
