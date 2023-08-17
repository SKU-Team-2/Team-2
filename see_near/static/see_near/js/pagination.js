document.addEventListener("DOMContentLoaded", function () {
  const pagination = document.getElementById("pagination");
  let currentPage = 1; // 현재 페이지 번호
  const totalPages = 9; // 전체 페이지 수

  function createPaginationItem(pageNumber, isActive) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.textContent = pageNumber;
    a.href = "#";
    a.classList.add("num");
    if (isActive) {
      a.classList.add("active");
    }
    li.appendChild(a);
    return li;
  }

  function updatePagination() {
    pagination.innerHTML = ""; // 기존 페이징 아이템 제거

    // 첫 페이지 및 이전 페이지 아이템 추가
    pagination.appendChild(createPaginationItem("처음 페이지"));
    pagination.appendChild(createPaginationItem("<<"));

    // 페이지 번호 아이템 추가
    for (let i = 1; i <= totalPages; i++) {
      pagination.appendChild(createPaginationItem(i, i === currentPage));
    }

    // 다음 페이지 및 마지막 페이지 아이템 추가
    pagination.appendChild(createPaginationItem(">>"));
    pagination.appendChild(createPaginationItem("끝 페이지"));
  }

  updatePagination(); // 초기 페이징 생성

  // 페이지 번호 클릭 이벤트 처리
  pagination.addEventListener("click", function (event) {
    event.preventDefault();

    const clickedItem = event.target;
    if (clickedItem.classList.contains("num")) {
      const newPage = parseInt(clickedItem.textContent);
      currentPage = newPage; // 현재 페이지 업데이트
      updatePagination();
      // TODO: 선택한 페이지에 맞는 데이터 로딩 등의 처리 수행
    }
  });
});
