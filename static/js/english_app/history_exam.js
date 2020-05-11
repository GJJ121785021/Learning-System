new Vue({
    el: '#history_exam',
    data: {
        datas: null
    },
    mounted() {
        this.get_history_exam()
    },
    methods: {
        get_history_exam: function () {
            axios
                .get(location.origin + '/english_app/api/history_exam.json')
                .then(response => this.datas = response.data)
                .catch(
                    function (error) {
                        console.log(error)
                    }
                )
        }
    },
})
