(function() {
    const form = document.getElementById('order');
    if (!form) return;

    const totalPriceEl = document.getElementById('totalPrice');
    const clientMsg = document.getElementById('clientMessage');
    const applyPromoBtn = document.getElementById('applyPromo');
    const payBtn = document.getElementById('payBtn');

    function showMessage(text, type='info') {
        if (!clientMsg) return;
        clientMsg.innerHTML = `<div class="alert alert-${type}">${text}</div>`;
    }

    function getCSRFToken() {
        const input = form.querySelector('input[name="csrfmiddlewaretoken"]');
        if (input) return input.value;
        const match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? match[1] : '';
    }

    function collectPayload() {
        const data = {};
        const fd = new FormData(form);
        data.duration = parseInt(fd.get('duration') || '0', 10);
        data.diet_type = fd.get('diet_type') || '';
        data.is_breakfast = !!fd.get('is_breakfast');
        data.is_lunch = !!fd.get('is_lunch');
        data.is_dinner = !!fd.get('is_dinner');
        data.is_dessert = !!fd.get('is_dessert');
        data.promo_code = (fd.get('promo_code') || '').trim();
        data.excluded_allergens = [];
        form.querySelectorAll('input[name="excluded_allergens"]:checked').forEach(ch => {
            const v = parseInt(ch.value, 10);
            if (!Number.isNaN(v)) data.excluded_allergens.push(v);
        });
        return data;
    }

    async function updatePrice() {
        const payload = collectPayload();
        try {
            const resp = await fetch('/api/promo/validate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                    'Accept': 'application/json'
                },
                credentials: 'same-origin',
                body: JSON.stringify(payload)
            });
            if (resp.status === 403) { return; }
            if (!resp.ok) {
                return;
            }
            const data = await resp.json();
            if (totalPriceEl) totalPriceEl.textContent = data.price || '00000';
            if (data.promo_applied) {
                showMessage('Промокод применён', 'success');
            } else if (payload.promo_code) {
                showMessage('Промокод не найден или не активен', 'secondary');
            } else {
                clientMsg.innerHTML = '';
            }
        } catch (e) { /* silent */ }
    }

    async function submitOrder(e) {
        e.preventDefault();
        const payload = collectPayload();
        if (payBtn) {
            payBtn.disabled = true;
            payBtn.textContent = 'Оформляем...';
        }
        try {
            const resp = await fetch('/api/order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                    'Accept': 'application/json'
                },
                credentials: 'same-origin',
                body: JSON.stringify(payload)
            });
            if (resp.status === 403) {
                showMessage('Нужно войти, чтобы оформить заказ.', 'warning');
                return;
            }
            if (!resp.ok) {
                const err = await resp.json().catch(() => ({}));
                const msgs = typeof err === 'object' ? JSON.stringify(err) : 'Ошибка оформления заказа';
                throw new Error(msgs);
            }
            const data = await resp.json();
            if (totalPriceEl) totalPriceEl.textContent = data.price || '00000';
            showMessage('Подписка оформлена. Стоимость: ' + (data.price || '—') + '₽', 'success');
        } catch (e) {
            showMessage(e.message || 'Ошибка', 'danger');
        } finally {
            if (payBtn) {
                payBtn.disabled = false;
                payBtn.textContent = 'Оплатить';
            }
        }
    }

    form.addEventListener('change', updatePrice);
    form.addEventListener('input', (ev) => {
        if (['promo_code'].includes(ev.target.name)) return;
        clearTimeout(window.__priceTimer);
        window.__priceTimer = setTimeout(updatePrice, 300);
    });
    if (applyPromoBtn) applyPromoBtn.addEventListener('click', updatePrice);
    form.addEventListener('submit', submitOrder);

    updatePrice();
})();
