========================
plone.app.portlets to-do
========================

  Decisions

    o May need a way to filter addable portlets by permission (e.g. some
        portlets are only available to some groups of users)

    o Category mappings are created on-the-fly in the namespace traversal
      adapters, which many not be ideal (even though these are protected by
      ManagePortal)

        - may be sufficient to create when the management views are invoked
