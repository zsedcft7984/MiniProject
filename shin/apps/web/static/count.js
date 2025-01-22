document.addEventListener('DOMContentLoaded', function() {
    const cartCount = document.getElementById('cart-count');

    // 페이지 로드 시 장바구니 개수를 가져와서 업데이트
    if (cartCount) {
        fetch('/web/get_cart_count')
            .then(response => response.json())
            .then(data => {
                cartCount.textContent = data.cart_count || 0;  // 기본값 0
            })
            .catch(error => {
                console.error('Error fetching cart count:', error);
            });
    }

    // 'add-to-cart' 버튼 클릭 시 처리
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const menuName = this.dataset.name;
            const itemType = this.dataset.type || "단품";  // 기본값으로 단품 지정
            addToCart(menuName, 1, itemType);
        });
    });

    // 서버에 상품 추가 요청 및 알림 표시
    function addToCart(menuName, quantity, itemType) {
        fetch('/web/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                menu_name: menuName,
                quantity: quantity,
                item_type: itemType
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                cartCount.textContent = data.cart_count;  // 장바구니 개수 업데이트
                alert(`"${menuName}(${itemType})"가 장바구니에 추가되었습니다.`);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
