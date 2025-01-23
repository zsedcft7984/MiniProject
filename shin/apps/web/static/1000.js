
    // 숫자에 쉼표 추가하는 함수
    function onlyNumberWithComma(obj) {
        obj.value = Number(obj.value.replace(/[^0-9]/g,'')).toLocaleString();
    }

    window.onload = function() {
        const quantityElements = document.querySelectorAll('.item-quantity');

        quantityElements.forEach(function(element) {
            const quantity = element.getAttribute('data-quantity');
            element.textContent = '₩ ' + Number(quantity.replace(/[^0-9]/g,'')).toLocaleString();
        });
    };
