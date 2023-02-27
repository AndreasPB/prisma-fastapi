<script lang="ts">
    import type { PageData } from './$types';
    
    export let data: PageData;
</script>

{#each data.users as user}
    <div>{user.name}</div>   
    {#each user.posts.slice(0, 5) as post}
        <div>{post.title}</div>   
    {/each}
{/each}