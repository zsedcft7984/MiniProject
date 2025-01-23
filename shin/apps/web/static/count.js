
document.addEventListener('DOMContentLoaded', function() {
    const cartCount = document.getElementById('cart-count');
    
    // 페이지 로드 시 장바구니 개수를 가져와서 업데이트
    if (cartCount) {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/web/get_cart_count', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                cartCount.textContent = data.cart_count || 0;  // 기본값 0
            } else if (xhr.readyState === 4) {
                console.error('Error fetching cart count:', xhr.status);
            }
        };
        xhr.send();
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
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/web/add_to_cart', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                if (data.success) {
                    cartCount.textContent = data.cart_count;  // 장바구니 개수 업데이트
                    alert(`"${menuName}(${itemType})"가 장바구니에 추가되었습니다.`);
                } else {
                    alert(data.message);
                }
            } else if (xhr.readyState === 4) {
                console.error('Error adding to cart:', xhr.status);
            }
        };
        const body = JSON.stringify({
            menu_name: menuName,
            quantity: quantity,
            item_type: itemType
        });
        xhr.send(body);
    }
});


