{ photo.date == null ?
    <br/>
    :
    <div className="card-title small">{Date(photo.date).toLocaleString()}</div>
}
