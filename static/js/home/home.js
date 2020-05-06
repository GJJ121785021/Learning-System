new Vue({
    el: '#check_app',
    data: {
        english_is_active: null,
        interview_is_active: null,
    },
    mounted() {
        if (location.pathname.match('english_app')) {
            this.english_is_active = 'active'
        } else if (location.pathname.match('interview_app')) {
            this.interview_is_active = 'active'
        }
    }
});