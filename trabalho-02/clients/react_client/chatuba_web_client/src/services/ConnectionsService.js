import axios from "axios";

export async function LoadConnectionsInfo(token) {
    const { connections } = await axios.get('http://localhost:8080/api/connections', {
        'Authorization': `Bearer ${token}`,
    });

    return connections;
}