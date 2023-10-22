<template>
    <div>
        <h1 style="margin-top: 5rem">Protected</h1>
        <h2>Name: {{ this.name }}</h2>
        <h2>Role: {{ this.role }}</h2>
    </div>
</template>

<script>
export default {
    data() {
        return {
            name: '',
            user: '',
            role: localStorage.getItem('role'),
        }
    },
    async mounted() {
        const res = await fetch('http://127.0.0.1:5000/protected', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
            }
        })

        const d = await res.json()
        if (res.ok) {
            console.log(d)
            this.name = d.name
        } else {
            alert(d.message)
            this.$router.push({ path: '/login' })
            console.log(d.msg)
        }
    }
}
</script>